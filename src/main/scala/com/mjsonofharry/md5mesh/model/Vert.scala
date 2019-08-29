package com.mjsonofharry.md5mesh.model

import atto._, Atto._
import cats.implicits._

case class Vert(
  index: Int,
  u: Double,
  v: Double,
  weightStart: Int,
  weightCount: Int
)

object Vert {
  val parser: Parser[Vert] = for {
    label <- string("vert") <~ spaceChar
    index <- int <~ spaceChar
    u <- double <~ spaceChar
    v <- double <~ spaceChar
    weightStart <- int <~ spaceChar
    weightCount <- int
  } yield Vert(
    index = index,
    u = u,
    v = v,
    weightStart = weightStart,
    weightCount = weightCount)
}