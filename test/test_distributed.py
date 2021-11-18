__copyright__ = """Copyright (C) 2021 University of Illinois Board of Trustees
"""

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from pyopencl.tools import (  # noqa
        pytest_generate_tests_for_pyopencl as pytest_generate_tests)
import pyopencl as cl
import numpy as np
import pytato as pt
import sys

from mpi4py import MPI  # pylint: disable=import-error
comm = MPI.COMM_WORLD

from pytato.distributed import (staple_distributed_send, make_distributed_recv,
    find_distributed_partition,
    execute_distributed_partition)

from pytato.partition import generate_code_for_partition


def test_distributed_execution_basic(ctx_factory):
    rank = comm.Get_rank()
    size = comm.Get_size()

    rng = np.random.default_rng()

    x_in = rng.integers(100, size=(4, 4))
    x = pt.make_data_wrapper(x_in)

    halo = staple_distributed_send(x, dest_rank=(rank-1) % size, comm_tag=42,
            stapled_to=make_distributed_recv(
                src_rank=(rank+1) % size, comm_tag=42, shape=(4, 4), dtype=int))

    y = x+halo

    # Find the partition
    outputs = pt.DictOfNamedArrays({"out": y})
    distributed_parts = find_distributed_partition(outputs)
    prg_per_partition = generate_code_for_partition(distributed_parts)

    # Execute the distributed partition
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    context = execute_distributed_partition(distributed_parts, prg_per_partition,
                                             queue, comm)

    final_res = [context[k] for k in outputs.keys()]

    np.testing.assert_allclose(x_in*2, final_res[0])


def test_distributed_execution_random_dag(ctx_factory):
    rank = comm.Get_rank()
    size = comm.Get_size()

    from testlib import RandomDAGContext, make_random_dag

    axis_len = 4

    ntests = 1
    for i in range(ntests):
        print(i)
        seed = 120 + i
        rdagc_pt = RandomDAGContext(np.random.default_rng(seed=seed),
                axis_len=axis_len, use_numpy=False)

        x = make_random_dag(rdagc_pt)

        halo = staple_distributed_send(x, dest_rank=(rank-1) % size, comm_tag=42,
            stapled_to=make_distributed_recv(
                src_rank=(rank+1) % size, comm_tag=42, shape=(4, 4), dtype=float))

        y = halo * 42

        res = staple_distributed_send(y, dest_rank=(rank-1) % size, comm_tag=43,
            stapled_to=make_distributed_recv(
                src_rank=(rank+1) % size, comm_tag=43, shape=(4, 4), dtype=float))

        dict_named_arys = pt.DictOfNamedArrays(
                    {"result": res})

        distributed_parts = find_distributed_partition(dict_named_arys)
        prg_per_partition = generate_code_for_partition(distributed_parts)

        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)

        context = execute_distributed_partition(distributed_parts, prg_per_partition,
                                                queue, comm)

        final_res = [context[k] for k in dict_named_arys.keys()]

        assert final_res


if __name__ == "__main__":
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from pytest import main
        main([__file__])
