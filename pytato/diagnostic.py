"""Pytato specific exceptions."""

__copyright__ = "Copyright (C) 2021 Kaushik Kulkarni"

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


__doc__ = """

Pytato-specific exceptions
--------------------------

.. autoclass:: NameClashError
.. autoclass:: CannotBroadcastError
.. autoclass:: UnknownIndexLambdaExpr
"""


class NameClashError(RuntimeError):
    """
    Raised when 2 non-identical :class:`~pytato.array.InputArgumentBase`'s are
    reachable in an :class:`~pytato.array.Array`'s DAG and share the same name. Here,
    we refer to 2 objects ``a`` and ``b`` as being identical iff ``a is b``.
    """


class CannotBroadcastError(ValueError):
    pass


class UnknownIndexLambdaExpr(ValueError):
    """
    Raised when the structure :class:`pytato.array.IndexLambda` could not be
    inferred.
    """
    pass
