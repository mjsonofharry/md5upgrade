package com.mjsonofharry.md5mesh.model

import atto._, Atto._
import cats.implicits._

case class Mesh(
  index: Int,
  shader: String,
  numverts: Int,
  numtris: Int,
  numweights: Int,
  verts: List[Vert],
  tris: List[Tri],
  weights: List[Weight]
)

object Mesh {
  val parser: Parser[Mesh] = for {
    index <- string("mesh") ~ spaceChar ~> 
      int <~ spaceChar ~ char('{') ~ many(whitespace)
    shader <- string("shader") ~ spaceChar ~ char('"') ~> 
      many(anyChar) <~ char('"') ~ many(whitespace)
    numverts <- string("numverts") ~ spaceChar ~> int <~ whitespace
    verts <- many(Vert.parser <~ whitespace) <~ whitespace
    numtris <- string("numtris") ~ spaceChar ~> int <~ whitespace
    tris <- many(Tri.parser <~ whitespace) <~ whitespace
    numweights <- string("numweights") ~ spaceChar ~> int <~ whitespace
    weights <- many(Weight.parser <~ whitespace) <~ whitespace <~ char('}')
  } yield Mesh(
    index = index,
    shader = shader.mkString,
    numverts = numverts,
    numtris = numtris,
    numweights = numweights,
    verts = verts,
    tris = tris,
    weights = weights,
  )
}