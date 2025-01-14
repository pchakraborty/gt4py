# -*- coding: utf-8 -*-
#
# Eve Toolchain - GT4Py Project - GridTools Framework
#
# Copyright (c) 2020, CSCS - Swiss National Supercomputing Center, ETH Zurich
# All rights reserved.
#
# This file is part of the GT4Py project and the GridTools framework.
# GT4Py is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later
# version. See the LICENSE.txt file at the top-level directory of this
# distribution for a copy of the license or check <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import enum
from typing import ClassVar, Dict, Generic, TypeVar

from pydantic import root_validator

from eve import GenericNode, IntEnum, Node, Str, StrEnum


class AssignmentKind(StrEnum):
    """Kind of assignment: plain or combined with operations."""

    PLAIN = "="
    ADD = "+="
    SUB = "-="
    MUL = "*="
    DIV = "/="


@enum.unique
class UnaryOperator(StrEnum):
    """Unary operator indentifier."""

    POS = "+"
    NEG = "-"


@enum.unique
class BinaryOperator(StrEnum):
    """Binary operator identifier."""

    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


@enum.unique
class DataType(IntEnum):
    """Data type identifier."""

    # IDs from dawn
    INVALID = 0
    AUTO = 1
    BOOLEAN = 2
    INT32 = 3
    FLOAT32 = 4
    FLOAT64 = 5
    UINT32 = 6


@enum.unique
class NativeFunction(StrEnum):
    ABS = "abs"
    MIN = "min"
    MAX = "max"
    MOD = "mod"

    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    ARCSIN = "arcsin"
    ARCCOS = "arccos"
    ARCTAN = "arctan"

    SQRT = "sqrt"
    EXP = "exp"
    LOG = "log"

    ISFINITE = "isfinite"
    ISINF = "isinf"
    ISNAN = "isnan"
    FLOOR = "floor"
    CEIL = "ceil"
    TRUNC = "trunc"

    IR_OP_TO_NUM_ARGS: ClassVar[Dict["NativeFunction", int]]

    @property
    def arity(self) -> int:
        return self.IR_OP_TO_NUM_ARGS[self]


NativeFunction.IR_OP_TO_NUM_ARGS = {
    NativeFunction.ABS: 1,
    NativeFunction.MIN: 2,
    NativeFunction.MAX: 2,
    NativeFunction.MOD: 2,
    NativeFunction.SIN: 1,
    NativeFunction.COS: 1,
    NativeFunction.TAN: 1,
    NativeFunction.ARCSIN: 1,
    NativeFunction.ARCCOS: 1,
    NativeFunction.ARCTAN: 1,
    NativeFunction.SQRT: 1,
    NativeFunction.EXP: 1,
    NativeFunction.LOG: 1,
    NativeFunction.ISFINITE: 1,
    NativeFunction.ISINF: 1,
    NativeFunction.ISNAN: 1,
    NativeFunction.FLOOR: 1,
    NativeFunction.CEIL: 1,
    NativeFunction.TRUNC: 1,
}


# TODO not really common
@enum.unique
class LoopOrder(IntEnum):
    """Loop order identifier."""

    FORWARD = 1
    BACKWARD = 2
    # PARALLEL = 3  # noqa


@enum.unique
class LocationType(IntEnum):
    Vertex = 0
    Edge = 1
    Cell = 2
    NoLocation = 3


@enum.unique
class VerticalLocationType(IntEnum):
    NoLocation = -1
    Horizontal = 0
    K = 1


@enum.unique
class BuiltInLiteral(IntEnum):
    MAX_VALUE = 0
    MIN_VALUE = 1
    ZERO = 2
    ONE = 3


ExprT = TypeVar("ExprT")


class Expr(Node):
    location_type: LocationType


class Stmt(Node):
    location_type: LocationType


class BinaryOp(Expr, GenericNode, Generic[ExprT]):
    op: BinaryOperator
    left: ExprT
    right: ExprT

    @root_validator(pre=True)
    def check_location_type(cls, values):
        if values["left"].location_type != values["right"].location_type:
            raise ValueError("Location type mismatch")

        if "location_type" not in values:
            values["location_type"] = values["left"].location_type
        elif values["left"].location_type != values["location_type"]:
            raise ValueError("Location type mismatch")

        return values


class Literal(Expr):
    value: Str
    vtype: DataType


LeftT = TypeVar("LeftT")


class AssignStmt(Stmt, GenericNode, Generic[LeftT, ExprT]):
    left: LeftT  # there are no local variables in gtir, only fields
    right: ExprT

    @root_validator(pre=True)
    def check_location_type(cls, values):
        if values["left"].location_type != values["right"].location_type:
            raise ValueError("Location type mismatch")

        if "location_type" not in values:
            values["location_type"] = values["left"].location_type
        elif values["left"].location_type != values["location_type"]:
            raise ValueError("Location type mismatch")

        return values
