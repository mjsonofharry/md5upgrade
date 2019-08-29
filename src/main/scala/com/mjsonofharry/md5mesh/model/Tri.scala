package com.mjsonofharry.md5mesh.model

import atto._, Atto._
import cats.implicits._

case class Tri(
  index: Int,
  verts: (Int, Int, Int)
)

object Tri {
  val parser: Parser[Tri] = for {
    label <- string("tri") <~ spaceChar
    index <- int <~ spaceChar
    v1 <- int <~ spaceChar
    v2 <- int <~ spaceChar
    v3 <- int
  } yield Tri(
    index = index,
    verts = (v1, v2, v3)
  )
}