---
version: 0.1.0
date: 2023-02-21
---

# Kemonomimi Grammar Specification

> **Warning** This specification is still in its development and formalization
> stage, while it should be useable to implement tooling with, it may possibly
> change drastically until a final version is ratified.

This document contains the formal specification defining the Kemonomimi context-free grammar for use in describing programming and other languages for human-computer use.

## Introduction

There are a large number of existing metasyntax languages for describing formal grammars, such as [EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form), and [ABNF](https://en.wikipedia.org/wiki/Augmented_Backus%E2%80%93Naur_form), however they all have their quirks and are not expressive as some people would like. What Kemonomimi aims to bring to the space of metasyntax and context-free grammar languages, is a more complete and useable syntax for cleanly defining things that are difficult to in other grammars, such as unicode support, ranges, and even to an extent some binary definition capability. This allows for you to write a more complete grammar that relies on less repetition, but is not as oblique as something like APL. In addition Kemonomimi has build-in facilities for reusability baked in, allowing for more complex grammars to be defined, all while not placing a large burden on the author of the grammar.

## Notation

This specification shares some of the notation used within the Kemonomimi language itself, but for normative reference, they will be briefly described here, along with other specification only notation.

> **Warning** DO NOT use the notation definitions in this section as implementation details for
> Kemonomimi notation that might look identical. The notation in this section only describes the
> use within this specification. Refer to the section of the specification that describes the notation
> for implementation.

### Unicode Codepoints

Throughout the standard, there will be codepoints from the Unicode standard referenced, they will follow the `U+XXXXXX` formatting, where the `XXXXXX` will be 6 hexadecimal digits.

The codepoints are specified in UTF-32 form with the `U+` prefix which is typical when specifying Unicode codepoints, even though that is not the expected encoding when implemented.

### Ranges

When referring to collections of things in sequential order, it is convenient to reference them in a way that is both more succinct, but also is clear, as such, in this specification the `...` operator will be used to indicate that a span of elements in a collection have been truncated.

It may be used between two ordinals such as `0 ... 9` to indicate a sequential progression from the first element to the last element, this is commonly used with numeric literals but also Unicode codepoints. It may also be at the end, specifying an un-bounded continuation, such as `0...`.


## Structure

Kemonomimi grammars consist of [UTF-8](https://www.unicode.org/versions/Unicode15.0.0/ch02.pdf#page=30) encoded characters, explicitly without a [BOM](https://en.wikipedia.org/wiki/Byte_order_mark) in the document due to how UTF-8 is endian agnostic.

The contents of which is a series of [statements](#statements) with surrounding [whitespace](#whitespace) which is then terminated by either an [EOF](https://en.wikipedia.org/wiki/End-of-file) no more statement definitions.

## Whitespace

Whitespace is defined as a specific set of codepoint ranges from the following [Unicode Categories](https://www.unicode.org/notes/tn36/):

 * `Zs` - Punctuation > Space
 * `Zp` - Paragraph Separator
 * `Zl` - Line Separator
 * `Cc` - Control Characters
 * `Cf` - Format

The codepoint ranges are as follows:

 * `U+000000 ... U+000020`
 * `U+0000A0`
 * `U+0000AD`
 * `U+000080 ... U+00009F`
 * `U+001680`
 * `U+002000 ... U+00200F`
 * `U+002028 ... U+00202F`
 * `U+00205F`
 * `U+002060`
 * `U+003000`

Whitespace in Kemonomimi is ignored and does not have an effect on the grammar, except in cases of multi-codepoint symbols such as identifiers or comment tokens.

## Syntax

The following sections define the overall syntax of the Kemonomimi language.

### Comments

Kemonomimi inherits the comment syntax from [EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form), that being that a comment is anything between a `(*` and  `*)` except for other comments, nesting is not permitted.

Example:
```kemonomimi

(* This is a single-line comment *)

(*
	This is a multi-line comment.

	It can contain anything but the start or end comment tokens.

	But, '( *' is valid because of the space
*)
```

### Strings

Strings are a series of zero or more valid UTF-8 codepoints except noted below surrounded by apostrophes (`'`) (A.K.A Single-quotation marks) as defined by Unicode codepoint `U+000027`.

In order to represent codepoints that are not easily produced via a keyboard, such as things like newlines, and also to include the ability to use the string delimiter itself in a string, Kemonomimi, like many other languages implements character escaping using the Reverse Solidus (`\`) (A.K.A backslash) character as defined by Unicode codepoint `U+00005C`.

The following escape sequences are recognized:

| Escape Sequence | Codepoint Represented | Comments                                        |
|-----------------|-----------------------|-------------------------------------------------|
| `\\`            | `U+00005C`            | Used to represent a literal `\` within a string |
| `\'`            | `U+000027`            | Used to represent a literal `'` within a string |
| `\t`            | `U+000009`            | Horizontal Tab                                  |
| `\n`            | `U+00000A`            | Line Feed                                       |
| `\v`            | `U+00000B`            | Vertical Tab                                    |
| `\f`            | `U+00000C`            | Form Feed                                       |
| `\r`            | `U+00000D`            | Carriage Return                                 |
| `\uXXXXXXXX`    | `U+XXXXXXXX`          | Raw Unicode hexadecimal codepoint (zero padded) |
| `\xXX`          | N/A                   | Raw Byte                                        |

With the `\uXXXXXX` escape sequence, you may specify anywhere between 1 and 8 hexadecimal numbers to indicate the desired codepoint. If less than 8 are specified, it is left-padded with zeros implicitly, making something such as `\u5C` actually represent `\u00005C`

Strings are classified as complete terminals, meaning that a string of two or more codepoints is the same as [rule](#rules) defining them individually.

Example:

```kemonomimi
'This is a valid string'

'Hello\nWorld'

'にゃ\u301C Jag älskar BLÅHAJ!'
```

### Identifiers

An identifier is used in constructing rules and referencing said rules, it consists of one or more Unicode codepoints from the following Unicode categories:

 * `Ll` - Lowercase Letter
 * `Lm` - Modified Letter
 * `Lo` - Other Letter
 * `Lt` - Titlecase Letter
 * `Lu` - Uppercase Letter
 * `Mc` - Spacing Mark
 * `Me` - Enclosing Mark
 * `Mn` - Non-spacing Mark
 * `Nd` - Decimal Number
 * `Nl` - Letter Number
 * `No` - Other Number
 * `Pc` - Punctuation > Connector

An Identifier **must not** start with any Unicode codepoint from the following Unicode categories:

 * `Mc` - Spacing Mark
 * `Me` - Enclosing Mark
 * `Mn` - Non-spacing Mark
 * `Nd` - Decimal Number
 * `Nl` - Letter Number
 * `No` - Other Number

Due to the sheer number of codepoints within that range, they are not specified here, you can find them in the [Identifier Codepoint](#appendix-1---identifier-unicode-codepoints) appendix.


### Numeric Literals

Some rule definitions require that a raw numeric literal be used, such as for [terminal repetition](#terminal-repetition), as such kemonomimi has support for numeric literals to be used as operands to supported grammar constructs.

A numeric literal is a sequence of at least one number from the range `U+000030...U+000039` within the Unicode Decimal Number category, those being in order; `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`.

There is no support for other than base-10 numerics, and no support for literal separators as there are in other languages, this is to discourage the use of using absurdly large numbers as in the context of a grammar they make little to no sense.

Example:

```kemonomimi
0
1234
```

### Raw Codepoint

When defining grammars, it is useful to explicitly define a codepoint you wish to use as a terminal, as such, Kemonomimi allows for you to do so, much in the same way as if you wish to do so in a [string](#strings). However rather than using the `\uXXXXXXXX` notation it uses the `U+XXXXXXXX` notation.

Just like with the escape sequence counterpart, it is left-padded with zeros, however there is an additional limitation that it must be specified in groups of 2 digits at a time, with up to 8 hexadecimal digits.

Example:

```kemonomimi
U+00
U+00AD
U+00202F
U+0001F248
```

### Uses Statement

In Kemonomimi there is only one reserved keyword, that being `uses`, this is to allow for the "import" of other grammars into the current document.

This lets you reference existing grammars that are part of the standardized Kemonomimi library, or for other grammars on the filesystem or via a URI. When you use this, it instructs any tooling to first ingest that used grammar, which will then effectively bring in all of the definitions it provided.

It is defined as the literal `uses` followed by a [string](#strings) which specifies path followed by the [rule terminator](#terminator) (`;`).

Lookup for `uses` statements is based on the contents of the string, it follows the general order as follows:

 1. Does the string end in `.mimi`
    1. If not, look for it in the standard fragment collection
    2. Otherwise go to 2
 2. Does the string start with `https`
    1. If so, it's a URI
    2. Otherwise, go to 3
 3. Assumed to be a local file path

In the case of local file paths, only Unix-like paths are supported, regardless of platform. Relative and absolute directory traversal is also supported when looking for the specified grammar fragment.

Example:
```kemonomimi

uses './local-file.mimi';
uses 'unicode';
uses 'https://example.com/stuff.mimi';

```

Due to the potential security issues involved, using a URI in a `uses` statement is optional and implementation dependent, so it's not advised to rely on it.

### Range

When referencing terminal literals, it is sometimes useful to be able to specify an inclusive range in which you'd like to match. Kemonomimi supplies this with the `...` syntax (three consecutive full-stops as specified by Unicode codepoint `U+00002E`), allowing you define a consecutive span.

This applies to both single-terminal strings (such as 'a') and Unicode codepoint literals (such as `U+000020`), and can be mixed, so long as the the starting terminal as represented by a Unicode codepoint is smaller than the ending terminal as represented by a Unicode codepoint.

The interpolation done by the `...` operation is purely linear and sequential, meaning that when using it, you can not specify things such as strides. To represent a stride, it must be broken into individual ranges.

There does not need to be a space between the terminals and the `...`, but it is recommended to improve readability.

Example:

```kemonomimi
'a' ... 'z'

'0'...U+000039
```

### Terminator

The terminator is a single `;` as represented by Unicode codepoint `U+00003B`, it is used to terminate the [`uses`](#uses-statement) statement and [rules](#rules).

It is valid to use `;` in a [string](#strings) such as `';'` as well as to use a Unicode codepoint terminal to represent it like `U+00003B` for use in rules as a terminal. The only point it has special meaning as a raw `;` within the Kemonomimi file.

### Terminal Concatenation

When constructing rules, it is necessary to define a linear sequence of terminals, for this the terminal concatenation is used.

### Terminal Repetition

Occasionally it is required that a terminal be repeated, for this, terminal repetition is used. There are three primary symbols used for this,`+`, `*`, and `?` (specified by Unicode codepoints `U+00002B`, `U+00002A`, and `U+00003F` respectively).

The `+` symbol suffixes a terminal to indicate that it is a repetition of *one or more* of that terminal. For example:

```kemonomimi
'a'+
(* Would match 'a', 'aa', 'aaa', etc. *)
```

The `*` symbol suffixes a terminal and then is followed by a [numeric literal](#numeric-literals) indicating the number of required repetitions. For example:

```kemonomimi
'b'*2
(* Only matches 'bb' *)
```
The `?` symbol, much like `*` suffixes a terminal and is then is followed by a [numeric literal](#numeric-literals), however in this case it represents the *maximum* number of repetitions. For Example:

```kemonomimi
'c'?3
(* Will match 'c', 'cc', 'ccc', but not 'cccc' etc *)

```


### Optional Groups

When specifying a grammar, it is useful to define one or more optional terminals inline with the rule, rather than explicitly specify two independent paths for a rule to denote an optional terminal.

Optional groups allow just this, any terminal sequence between `[` and `]` (specified by Unicode codepoints `U+00005B` and `U+00005D` respectively) is optionally applied to the rule.

Example:
```kemonomimi
'a' [ 'b' ] 'c'
(* Would match for 'abc' and 'ac' *)
```

### Terminal Groups

Sometimes it's useful to define a small group of terminals that don't warrant a dedicated rule of their own, as such, terminals within `(` and `)` (specified by Unicode codepoints `U+000028` and `U+000029` respectively) will be treated as if they were a rule.

Example:
```kemonomimi
( 'a' | 'z'+ )
( '0'...'9' | '_' )*
```

### Rules

Rules are the foundation of any context-free grammar, this is no different in Kemonomimi. They are defined by specifying an [identifier](#identifiers), followed by the `=` character (specified by Unicode codepoint `U+00003D`), which itself is followed by one or more terminals, and finally ended with a [rule terminator](#terminator).

Rules may span multiple lines, so long as they end with a `;`.


The root rule for the grammar is defined by a rule name enclosed between `<` and `>` (specified by Unicode codepoints `U+00003C` and `U+00003E` respectively). The root rule defines the main entrypoint to the grammar as the root of the parse tree.

Example:

```kemonomimi

letters = 'a' ... 'z' | 'Z' ... 'Z' ;

hex_digit = '0' ... '9' | 'a' ... 'z' | 'A' ... 'Z' ;
hex_number = '0x' (hex_digit | '_')+ ;

sign = '-' | '+' ;
numbers = '0' ... '9' ;

signed_number = [ sign ] number+ ;

<numbers> = ( signed_number )+ ;

```

## Evaluation

The evaluation order for Kemonomimi grammars is much like other context-free grammars, which is traditionally top-down, with rules building upon one another.

All [`uses`](#uses-statement) statements are evaluated first, as any grammar fragments in the referenced files might be referenced in the parent grammar definition.

## Appendices

### Appendix 1 - Identifier Unicode codepoints

The following table shows all of the valid Unicode codepoints that may be used to construct [identifiers](#identifiers).

> **Warning** This table also includes the Unicode codepoints that are **not allowed** as the
> starting codepoint

|                       |                       |                       |                       |
|-----------------------|-----------------------|-----------------------|-----------------------|
| `U+000030...U+000039` | `U+000041...U+00005A` | `U+00005F           ` | `U+000061...U+00007A` |
| `U+0000AA           ` | `U+0000B2           ` | `U+0000B3           ` | `U+0000B5           ` |
| `U+0000B9           ` | `U+0000BA           ` | `U+0000BC...U+0000BE` | `U+0000C0...U+0000D6` |
| `U+0000D8...U+0000F6` | `U+0000F8...U+0002C1` | `U+0002C6...U+0002D1` | `U+0002E0...U+0002E4` |
| `U+0002EC           ` | `U+0002EE           ` | `U+000300...U+000374` | `U+000376           ` |
| `U+000377           ` | `U+00037A...U+00037D` | `U+00037F           ` | `U+000386           ` |
| `U+000388...U+00038A` | `U+00038C           ` | `U+00038E...U+0003A1` | `U+0003A3...U+0003F5` |
| `U+0003F7...U+000481` | `U+000483...U+00052F` | `U+000531...U+000556` | `U+000559           ` |
| `U+000560...U+000588` | `U+000591...U+0005BD` | `U+0005BF           ` | `U+0005C1           ` |
| `U+0005C2           ` | `U+0005C4           ` | `U+0005C5           ` | `U+0005C7           ` |
| `U+0005D0...U+0005EA` | `U+0005EF...U+0005F2` | `U+000610...U+00061A` | `U+000620...U+000669` |
| `U+00066E...U+0006D3` | `U+0006D5...U+0006DC` | `U+0006DF...U+0006E8` | `U+0006EA...U+0006FC` |
| `U+0006FF           ` | `U+000710...U+00074A` | `U+00074D...U+0007B1` | `U+0007C0...U+0007F5` |
| `U+0007FA           ` | `U+0007FD           ` | `U+000800...U+00082D` | `U+000840...U+00085B` |
| `U+000860...U+00086A` | `U+000870...U+000887` | `U+000889...U+00088E` | `U+000898...U+0008E1` |
| `U+0008E3...U+000963` | `U+000966...U+00096F` | `U+000971...U+000983` | `U+000985...U+00098C` |
| `U+00098F           ` | `U+000990           ` | `U+000993...U+0009A8` | `U+0009AA...U+0009B0` |
| `U+0009B2           ` | `U+0009B6...U+0009B9` | `U+0009BC...U+0009C4` | `U+0009C7           ` |
| `U+0009C8           ` | `U+0009CB...U+0009CE` | `U+0009D7           ` | `U+0009DC           ` |
| `U+0009DD           ` | `U+0009DF...U+0009E3` | `U+0009E6...U+0009F1` | `U+0009F4...U+0009F9` |
| `U+0009FC           ` | `U+0009FE           ` | `U+000A01...U+000A03` | `U+000A05...U+000A0A` |
| `U+000A0F           ` | `U+000A10           ` | `U+000A13...U+000A28` | `U+000A2A...U+000A30` |
| `U+000A32           ` | `U+000A33           ` | `U+000A35           ` | `U+000A36           ` |
| `U+000A38           ` | `U+000A39           ` | `U+000A3C           ` | `U+000A3E...U+000A42` |
| `U+000A47           ` | `U+000A48           ` | `U+000A4B...U+000A4D` | `U+000A51           ` |
| `U+000A59...U+000A5C` | `U+000A5E           ` | `U+000A66...U+000A75` | `U+000A81...U+000A83` |
| `U+000A85...U+000A8D` | `U+000A8F...U+000A91` | `U+000A93...U+000AA8` | `U+000AAA...U+000AB0` |
| `U+000AB2           ` | `U+000AB3           ` | `U+000AB5...U+000AB9` | `U+000ABC...U+000AC5` |
| `U+000AC7...U+000AC9` | `U+000ACB...U+000ACD` | `U+000AD0           ` | `U+000AE0...U+000AE3` |
| `U+000AE6...U+000AEF` | `U+000AF9...U+000AFF` | `U+000B01...U+000B03` | `U+000B05...U+000B0C` |
| `U+000B0F           ` | `U+000B10           ` | `U+000B13...U+000B28` | `U+000B2A...U+000B30` |
| `U+000B32           ` | `U+000B33           ` | `U+000B35...U+000B39` | `U+000B3C...U+000B44` |
| `U+000B47           ` | `U+000B48           ` | `U+000B4B...U+000B4D` | `U+000B55...U+000B57` |
| `U+000B5C           ` | `U+000B5D           ` | `U+000B5F...U+000B63` | `U+000B66...U+000B6F` |
| `U+000B71...U+000B77` | `U+000B82           ` | `U+000B83           ` | `U+000B85...U+000B8A` |
| `U+000B8E...U+000B90` | `U+000B92...U+000B95` | `U+000B99           ` | `U+000B9A           ` |
| `U+000B9C           ` | `U+000B9E           ` | `U+000B9F           ` | `U+000BA3           ` |
| `U+000BA4           ` | `U+000BA8...U+000BAA` | `U+000BAE...U+000BB9` | `U+000BBE...U+000BC2` |
| `U+000BC6...U+000BC8` | `U+000BCA...U+000BCD` | `U+000BD0           ` | `U+000BD7           ` |
| `U+000BE6...U+000BF2` | `U+000C00...U+000C0C` | `U+000C0E...U+000C10` | `U+000C12...U+000C28` |
| `U+000C2A...U+000C39` | `U+000C3C...U+000C44` | `U+000C46...U+000C48` | `U+000C4A...U+000C4D` |
| `U+000C55           ` | `U+000C56           ` | `U+000C58...U+000C5A` | `U+000C5D           ` |
| `U+000C60...U+000C63` | `U+000C66...U+000C6F` | `U+000C78...U+000C7E` | `U+000C80...U+000C83` |
| `U+000C85...U+000C8C` | `U+000C8E...U+000C90` | `U+000C92...U+000CA8` | `U+000CAA...U+000CB3` |
| `U+000CB5...U+000CB9` | `U+000CBC...U+000CC4` | `U+000CC6...U+000CC8` | `U+000CCA...U+000CCD` |
| `U+000CD5           ` | `U+000CD6           ` | `U+000CDD           ` | `U+000CDE           ` |
| `U+000CE0...U+000CE3` | `U+000CE6...U+000CEF` | `U+000CF1...U+000CF3` | `U+000D00...U+000D0C` |
| `U+000D0E...U+000D10` | `U+000D12...U+000D44` | `U+000D46...U+000D48` | `U+000D4A...U+000D4E` |
| `U+000D54...U+000D63` | `U+000D66...U+000D78` | `U+000D7A...U+000D7F` | `U+000D81...U+000D83` |
| `U+000D85...U+000D96` | `U+000D9A...U+000DB1` | `U+000DB3...U+000DBB` | `U+000DBD           ` |
| `U+000DC0...U+000DC6` | `U+000DCA           ` | `U+000DCF...U+000DD4` | `U+000DD6           ` |
| `U+000DD8...U+000DDF` | `U+000DE6...U+000DEF` | `U+000DF2           ` | `U+000DF3           ` |
| `U+000E01...U+000E3A` | `U+000E40...U+000E4E` | `U+000E50...U+000E59` | `U+000E81           ` |
| `U+000E82           ` | `U+000E84           ` | `U+000E86...U+000E8A` | `U+000E8C...U+000EA3` |
| `U+000EA5           ` | `U+000EA7...U+000EBD` | `U+000EC0...U+000EC4` | `U+000EC6           ` |
| `U+000EC8...U+000ECE` | `U+000ED0...U+000ED9` | `U+000EDC...U+000EDF` | `U+000F00           ` |
| `U+000F18           ` | `U+000F19           ` | `U+000F20...U+000F33` | `U+000F35           ` |
| `U+000F37           ` | `U+000F39           ` | `U+000F3E...U+000F47` | `U+000F49...U+000F6C` |
| `U+000F71...U+000F84` | `U+000F86...U+000F97` | `U+000F99...U+000FBC` | `U+000FC6           ` |
| `U+001000...U+001049` | `U+001050...U+00109D` | `U+0010A0...U+0010C5` | `U+0010C7           ` |
| `U+0010CD           ` | `U+0010D0...U+0010FA` | `U+0010FC...U+001248` | `U+00124A...U+00124D` |
| `U+001250...U+001256` | `U+001258           ` | `U+00125A...U+00125D` | `U+001260...U+001288` |
| `U+00128A...U+00128D` | `U+001290...U+0012B0` | `U+0012B2...U+0012B5` | `U+0012B8...U+0012BE` |
| `U+0012C0           ` | `U+0012C2...U+0012C5` | `U+0012C8...U+0012D6` | `U+0012D8...U+001310` |
| `U+001312...U+001315` | `U+001318...U+00135A` | `U+00135D...U+00135F` | `U+001369...U+00137C` |
| `U+001380...U+00138F` | `U+0013A0...U+0013F5` | `U+0013F8...U+0013FD` | `U+001401...U+00166C` |
| `U+00166F...U+00167F` | `U+001681...U+00169A` | `U+0016A0...U+0016EA` | `U+0016EE...U+0016F8` |
| `U+001700...U+001715` | `U+00171F...U+001734` | `U+001740...U+001753` | `U+001760...U+00176C` |
| `U+00176E...U+001770` | `U+001772           ` | `U+001773           ` | `U+001780...U+0017D3` |
| `U+0017D7           ` | `U+0017DC           ` | `U+0017DD           ` | `U+0017E0...U+0017E9` |
| `U+0017F0...U+0017F9` | `U+00180B...U+00180D` | `U+00180F...U+001819` | `U+001820...U+001878` |
| `U+001880...U+0018AA` | `U+0018B0...U+0018F5` | `U+001900...U+00191E` | `U+001920...U+00192B` |
| `U+001930...U+00193B` | `U+001946...U+00196D` | `U+001970...U+001974` | `U+001980...U+0019AB` |
| `U+0019B0...U+0019C9` | `U+0019D0...U+0019DA` | `U+001A00...U+001A1B` | `U+001A20...U+001A5E` |
| `U+001A60...U+001A7C` | `U+001A7F...U+001A89` | `U+001A90...U+001A99` | `U+001AA7           ` |
| `U+001AB0...U+001ACE` | `U+001B00...U+001B4C` | `U+001B50...U+001B59` | `U+001B6B...U+001B73` |
| `U+001B80...U+001BF3` | `U+001C00...U+001C37` | `U+001C40...U+001C49` | `U+001C4D...U+001C7D` |
| `U+001C80...U+001C88` | `U+001C90...U+001CBA` | `U+001CBD...U+001CBF` | `U+001CD0...U+001CD2` |
| `U+001CD4...U+001CFA` | `U+001D00...U+001F15` | `U+001F18...U+001F1D` | `U+001F20...U+001F45` |
| `U+001F48...U+001F4D` | `U+001F50...U+001F57` | `U+001F59           ` | `U+001F5B           ` |
| `U+001F5D           ` | `U+001F5F...U+001F7D` | `U+001F80...U+001FB4` | `U+001FB6...U+001FBC` |
| `U+001FBE           ` | `U+001FC2...U+001FC4` | `U+001FC6...U+001FCC` | `U+001FD0...U+001FD3` |
| `U+001FD6...U+001FDB` | `U+001FE0...U+001FEC` | `U+001FF2...U+001FF4` | `U+001FF6...U+001FFC` |
| `U+00203F           ` | `U+002040           ` | `U+002054           ` | `U+002070           ` |
| `U+002071           ` | `U+002074...U+002079` | `U+00207F...U+002089` | `U+002090...U+00209C` |
| `U+0020D0...U+0020F0` | `U+002102           ` | `U+002107           ` | `U+00210A...U+002113` |
| `U+002115           ` | `U+002119...U+00211D` | `U+002124           ` | `U+002126           ` |
| `U+002128           ` | `U+00212A...U+00212D` | `U+00212F...U+002139` | `U+00213C...U+00213F` |
| `U+002145...U+002149` | `U+00214E           ` | `U+002150...U+002189` | `U+002460...U+00249B` |
| `U+0024EA...U+0024FF` | `U+002776...U+002793` | `U+002C00...U+002CE4` | `U+002CEB...U+002CF3` |
| `U+002CFD           ` | `U+002D00...U+002D25` | `U+002D27           ` | `U+002D2D           ` |
| `U+002D30...U+002D67` | `U+002D6F           ` | `U+002D7F...U+002D96` | `U+002DA0...U+002DA6` |
| `U+002DA8...U+002DAE` | `U+002DB0...U+002DB6` | `U+002DB8...U+002DBE` | `U+002DC0...U+002DC6` |
| `U+002DC8...U+002DCE` | `U+002DD0...U+002DD6` | `U+002DD8...U+002DDE` | `U+002DE0...U+002DFF` |
| `U+002E2F           ` | `U+003005...U+003007` | `U+003021...U+00302F` | `U+003031...U+003035` |
| `U+003038...U+00303C` | `U+003041...U+003096` | `U+003099           ` | `U+00309A           ` |
| `U+00309D...U+00309F` | `U+0030A1...U+0030FA` | `U+0030FC...U+0030FF` | `U+003105...U+00312F` |
| `U+003131...U+00318E` | `U+003192...U+003195` | `U+0031A0...U+0031BF` | `U+0031F0...U+0031FF` |
| `U+003220...U+003229` | `U+003248...U+00324F` | `U+003251...U+00325F` | `U+003280...U+003289` |
| `U+0032B1...U+0032BF` | `U+003400           ` | `U+004DBF           ` | `U+004E00           ` |
| `U+009FFF...U+00A48C` | `U+00A4D0...U+00A4FD` | `U+00A500...U+00A60C` | `U+00A610...U+00A62B` |
| `U+00A640...U+00A672` | `U+00A674...U+00A67D` | `U+00A67F...U+00A6F1` | `U+00A717...U+00A71F` |
| `U+00A722...U+00A788` | `U+00A78B...U+00A7CA` | `U+00A7D0           ` | `U+00A7D1           ` |
| `U+00A7D3           ` | `U+00A7D5...U+00A7D9` | `U+00A7F2...U+00A827` | `U+00A82C           ` |
| `U+00A830...U+00A835` | `U+00A840...U+00A873` | `U+00A880...U+00A8C5` | `U+00A8D0...U+00A8D9` |
| `U+00A8E0...U+00A8F7` | `U+00A8FB           ` | `U+00A8FD...U+00A92D` | `U+00A930...U+00A953` |
| `U+00A960...U+00A97C` | `U+00A980...U+00A9C0` | `U+00A9CF...U+00A9D9` | `U+00A9E0...U+00A9FE` |
| `U+00AA00...U+00AA36` | `U+00AA40...U+00AA4D` | `U+00AA50...U+00AA59` | `U+00AA60...U+00AA76` |
| `U+00AA7A...U+00AAC2` | `U+00AADB...U+00AADD` | `U+00AAE0...U+00AAEF` | `U+00AAF2...U+00AAF6` |
| `U+00AB01...U+00AB06` | `U+00AB09...U+00AB0E` | `U+00AB11...U+00AB16` | `U+00AB20...U+00AB26` |
| `U+00AB28...U+00AB2E` | `U+00AB30...U+00AB5A` | `U+00AB5C...U+00AB69` | `U+00AB70...U+00ABEA` |
| `U+00ABEC           ` | `U+00ABED           ` | `U+00ABF0...U+00ABF9` | `U+00AC00           ` |
| `U+00D7A3           ` | `U+00D7B0...U+00D7C6` | `U+00D7CB...U+00D7FB` | `U+00F900...U+00FA6D` |
| `U+00FA70...U+00FAD9` | `U+00FB00...U+00FB06` | `U+00FB13...U+00FB17` | `U+00FB1D...U+00FB28` |
| `U+00FB2A...U+00FB36` | `U+00FB38...U+00FB3C` | `U+00FB3E           ` | `U+00FB40           ` |
| `U+00FB41           ` | `U+00FB43           ` | `U+00FB44           ` | `U+00FB46...U+00FBB1` |
| `U+00FBD3...U+00FD3D` | `U+00FD50...U+00FD8F` | `U+00FD92...U+00FDC7` | `U+00FDF0...U+00FDFB` |
| `U+00FE00...U+00FE0F` | `U+00FE20...U+00FE2F` | `U+00FE33           ` | `U+00FE34           ` |
| `U+00FE4D...U+00FE4F` | `U+00FE70...U+00FE74` | `U+00FE76...U+00FEFC` | `U+00FF10...U+00FF19` |
| `U+00FF21...U+00FF3A` | `U+00FF3F           ` | `U+00FF41...U+00FF5A` | `U+00FF66...U+00FFBE` |
| `U+00FFC2...U+00FFC7` | `U+00FFCA...U+00FFCF` | `U+00FFD2...U+00FFD7` | `U+00FFDA...U+00FFDC` |
| `U+010000...U+01000B` | `U+01000D...U+010026` | `U+010028...U+01003A` | `U+01003C           ` |
| `U+01003D           ` | `U+01003F...U+01004D` | `U+010050...U+01005D` | `U+010080...U+0100FA` |
| `U+010107...U+010133` | `U+010140...U+010178` | `U+01018A           ` | `U+01018B           ` |
| `U+0101FD           ` | `U+010280...U+01029C` | `U+0102A0...U+0102D0` | `U+0102E0...U+0102FB` |
| `U+010300...U+010323` | `U+01032D...U+01034A` | `U+010350...U+01037A` | `U+010380...U+01039D` |
| `U+0103A0...U+0103C3` | `U+0103C8...U+0103CF` | `U+0103D1...U+0103D5` | `U+010400...U+01049D` |
| `U+0104A0...U+0104A9` | `U+0104B0...U+0104D3` | `U+0104D8...U+0104FB` | `U+010500...U+010527` |
| `U+010530...U+010563` | `U+010570...U+01057A` | `U+01057C...U+01058A` | `U+01058C...U+010592` |
| `U+010594           ` | `U+010595           ` | `U+010597...U+0105A1` | `U+0105A3...U+0105B1` |
| `U+0105B3...U+0105B9` | `U+0105BB           ` | `U+0105BC           ` | `U+010600...U+010736` |
| `U+010740...U+010755` | `U+010760...U+010767` | `U+010780...U+010785` | `U+010787...U+0107B0` |
| `U+0107B2...U+0107BA` | `U+010800...U+010805` | `U+010808           ` | `U+01080A...U+010835` |
| `U+010837           ` | `U+010838           ` | `U+01083C           ` | `U+01083F...U+010855` |
| `U+010858...U+010876` | `U+010879...U+01089E` | `U+0108A7...U+0108AF` | `U+0108E0...U+0108F2` |
| `U+0108F4           ` | `U+0108F5           ` | `U+0108FB...U+01091B` | `U+010920...U+010939` |
| `U+010980...U+0109B7` | `U+0109BC...U+0109CF` | `U+0109D2...U+010A03` | `U+010A05           ` |
| `U+010A06           ` | `U+010A0C...U+010A13` | `U+010A15...U+010A17` | `U+010A19...U+010A35` |
| `U+010A38...U+010A3A` | `U+010A3F...U+010A48` | `U+010A60...U+010A7E` | `U+010A80...U+010A9F` |
| `U+010AC0...U+010AC7` | `U+010AC9...U+010AE6` | `U+010AEB...U+010AEF` | `U+010B00...U+010B35` |
| `U+010B40...U+010B55` | `U+010B58...U+010B72` | `U+010B78...U+010B91` | `U+010BA9...U+010BAF` |
| `U+010C00...U+010C48` | `U+010C80...U+010CB2` | `U+010CC0...U+010CF2` | `U+010CFA...U+010D27` |
| `U+010D30...U+010D39` | `U+010E60...U+010E7E` | `U+010E80...U+010EA9` | `U+010EAB           ` |
| `U+010EAC           ` | `U+010EB0           ` | `U+010EB1           ` | `U+010EFD...U+010F27` |
| `U+010F30...U+010F54` | `U+010F70...U+010F85` | `U+010FB0...U+010FCB` | `U+010FE0...U+010FF6` |
| `U+011000...U+011046` | `U+011052...U+011075` | `U+01107F...U+0110BA` | `U+0110C2           ` |
| `U+0110D0...U+0110E8` | `U+0110F0...U+0110F9` | `U+011100...U+011134` | `U+011136...U+01113F` |
| `U+011144...U+011147` | `U+011150...U+011173` | `U+011176           ` | `U+011180...U+0111C4` |
| `U+0111C9...U+0111CC` | `U+0111CE...U+0111DA` | `U+0111DC           ` | `U+0111E1...U+0111F4` |
| `U+011200...U+011211` | `U+011213...U+011237` | `U+01123E...U+011241` | `U+011280...U+011286` |
| `U+011288           ` | `U+01128A...U+01128D` | `U+01128F...U+01129D` | `U+01129F...U+0112A8` |
| `U+0112B0...U+0112EA` | `U+0112F0...U+0112F9` | `U+011300...U+011303` | `U+011305...U+01130C` |
| `U+01130F           ` | `U+011310           ` | `U+011313...U+011328` | `U+01132A...U+011330` |
| `U+011332           ` | `U+011333           ` | `U+011335...U+011339` | `U+01133B...U+011344` |
| `U+011347           ` | `U+011348           ` | `U+01134B...U+01134D` | `U+011350           ` |
| `U+011357           ` | `U+01135D...U+011363` | `U+011366...U+01136C` | `U+011370...U+011374` |
| `U+011400...U+01144A` | `U+011450...U+011459` | `U+01145E...U+011461` | `U+011480...U+0114C5` |
| `U+0114C7           ` | `U+0114D0...U+0114D9` | `U+011580...U+0115B5` | `U+0115B8...U+0115C0` |
| `U+0115D8...U+0115DD` | `U+011600...U+011640` | `U+011644           ` | `U+011650...U+011659` |
| `U+011680...U+0116B8` | `U+0116C0...U+0116C9` | `U+011700...U+01171A` | `U+01171D...U+01172B` |
| `U+011730...U+01173B` | `U+011740...U+011746` | `U+011800...U+01183A` | `U+0118A0...U+0118F2` |
| `U+0118FF...U+011906` | `U+011909           ` | `U+01190C...U+011913` | `U+011915           ` |
| `U+011916           ` | `U+011918...U+011935` | `U+011937           ` | `U+011938           ` |
| `U+01193B...U+011943` | `U+011950...U+011959` | `U+0119A0...U+0119A7` | `U+0119AA...U+0119D7` |
| `U+0119DA...U+0119E1` | `U+0119E3           ` | `U+0119E4           ` | `U+011A00...U+011A3E` |
| `U+011A47           ` | `U+011A50...U+011A99` | `U+011A9D           ` | `U+011AB0...U+011AF8` |
| `U+011C00...U+011C08` | `U+011C0A...U+011C36` | `U+011C38...U+011C40` | `U+011C50...U+011C6C` |
| `U+011C72...U+011C8F` | `U+011C92...U+011CA7` | `U+011CA9...U+011CB6` | `U+011D00...U+011D06` |
| `U+011D08           ` | `U+011D09           ` | `U+011D0B...U+011D36` | `U+011D3A           ` |
| `U+011D3C           ` | `U+011D3D           ` | `U+011D3F...U+011D47` | `U+011D50...U+011D59` |
| `U+011D60...U+011D65` | `U+011D67           ` | `U+011D68           ` | `U+011D6A...U+011D8E` |
| `U+011D90           ` | `U+011D91           ` | `U+011D93...U+011D98` | `U+011DA0...U+011DA9` |
| `U+011EE0...U+011EF6` | `U+011F00...U+011F10` | `U+011F12...U+011F3A` | `U+011F3E...U+011F42` |
| `U+011F50...U+011F59` | `U+011FB0           ` | `U+011FC0...U+011FD4` | `U+012000...U+012399` |
| `U+012400...U+01246E` | `U+012480...U+012543` | `U+012F90...U+012FF0` | `U+013000...U+01342F` |
| `U+013440...U+013455` | `U+014400...U+014646` | `U+016800...U+016A38` | `U+016A40...U+016A5E` |
| `U+016A60...U+016A69` | `U+016A70...U+016ABE` | `U+016AC0...U+016AC9` | `U+016AD0...U+016AED` |
| `U+016AF0...U+016AF4` | `U+016B00...U+016B36` | `U+016B40...U+016B43` | `U+016B50...U+016B59` |
| `U+016B5B...U+016B61` | `U+016B63...U+016B77` | `U+016B7D...U+016B8F` | `U+016E40...U+016E96` |
| `U+016F00...U+016F4A` | `U+016F4F...U+016F87` | `U+016F8F...U+016F9F` | `U+016FE0           ` |
| `U+016FE1           ` | `U+016FE3           ` | `U+016FE4           ` | `U+016FF0           ` |
| `U+016FF1           ` | `U+017000           ` | `U+0187F7           ` | `U+018800...U+018CD5` |
| `U+018D00           ` | `U+018D08           ` | `U+01AFF0...U+01AFF3` | `U+01AFF5...U+01AFFB` |
| `U+01AFFD           ` | `U+01AFFE           ` | `U+01B000...U+01B122` | `U+01B132           ` |
| `U+01B150...U+01B152` | `U+01B155           ` | `U+01B164...U+01B167` | `U+01B170...U+01B2FB` |
| `U+01BC00...U+01BC6A` | `U+01BC70...U+01BC7C` | `U+01BC80...U+01BC88` | `U+01BC90...U+01BC99` |
| `U+01BC9D           ` | `U+01BC9E           ` | `U+01CF00...U+01CF2D` | `U+01CF30...U+01CF46` |
| `U+01D165...U+01D169` | `U+01D16D...U+01D172` | `U+01D17B...U+01D182` | `U+01D185...U+01D18B` |
| `U+01D1AA...U+01D1AD` | `U+01D242...U+01D244` | `U+01D2C0...U+01D2D3` | `U+01D2E0...U+01D2F3` |
| `U+01D360...U+01D378` | `U+01D400...U+01D454` | `U+01D456...U+01D49C` | `U+01D49E           ` |
| `U+01D49F           ` | `U+01D4A2           ` | `U+01D4A5           ` | `U+01D4A6           ` |
| `U+01D4A9...U+01D4AC` | `U+01D4AE...U+01D4B9` | `U+01D4BB           ` | `U+01D4BD...U+01D4C3` |
| `U+01D4C5...U+01D505` | `U+01D507...U+01D50A` | `U+01D50D...U+01D514` | `U+01D516...U+01D51C` |
| `U+01D51E...U+01D539` | `U+01D53B...U+01D53E` | `U+01D540...U+01D544` | `U+01D546           ` |
| `U+01D54A...U+01D550` | `U+01D552...U+01D6A5` | `U+01D6A8...U+01D6C0` | `U+01D6C2...U+01D6DA` |
| `U+01D6DC...U+01D6FA` | `U+01D6FC...U+01D714` | `U+01D716...U+01D734` | `U+01D736...U+01D74E` |
| `U+01D750...U+01D76E` | `U+01D770...U+01D788` | `U+01D78A...U+01D7A8` | `U+01D7AA...U+01D7C2` |
| `U+01D7C4...U+01D7CB` | `U+01D7CE...U+01D7FF` | `U+01DA00...U+01DA36` | `U+01DA3B...U+01DA6C` |
| `U+01DA75           ` | `U+01DA84           ` | `U+01DA9B...U+01DA9F` | `U+01DAA1...U+01DAAF` |
| `U+01DF00...U+01DF1E` | `U+01DF25...U+01DF2A` | `U+01E000...U+01E006` | `U+01E008...U+01E018` |
| `U+01E01B...U+01E021` | `U+01E023           ` | `U+01E024           ` | `U+01E026...U+01E02A` |
| `U+01E030...U+01E06D` | `U+01E08F           ` | `U+01E100...U+01E12C` | `U+01E130...U+01E13D` |
| `U+01E140...U+01E149` | `U+01E14E           ` | `U+01E290...U+01E2AE` | `U+01E2C0...U+01E2F9` |
| `U+01E4D0...U+01E4F9` | `U+01E7E0...U+01E7E6` | `U+01E7E8...U+01E7EB` | `U+01E7ED           ` |
| `U+01E7EE           ` | `U+01E7F0...U+01E7FE` | `U+01E800...U+01E8C4` | `U+01E8C7...U+01E8D6` |
| `U+01E900...U+01E94B` | `U+01E950...U+01E959` | `U+01EC71...U+01ECAB` | `U+01ECAD...U+01ECAF` |
| `U+01ECB1...U+01ECB4` | `U+01ED01...U+01ED2D` | `U+01ED2F...U+01ED3D` | `U+01EE00...U+01EE03` |
| `U+01EE05...U+01EE1F` | `U+01EE21           ` | `U+01EE22           ` | `U+01EE24           ` |
| `U+01EE27           ` | `U+01EE29...U+01EE32` | `U+01EE34...U+01EE37` | `U+01EE39           ` |
| `U+01EE3B           ` | `U+01EE42           ` | `U+01EE47           ` | `U+01EE49           ` |
| `U+01EE4B           ` | `U+01EE4D...U+01EE4F` | `U+01EE51           ` | `U+01EE52           ` |
| `U+01EE54           ` | `U+01EE57           ` | `U+01EE59           ` | `U+01EE5B           ` |
| `U+01EE5D           ` | `U+01EE5F           ` | `U+01EE61           ` | `U+01EE62           ` |
| `U+01EE64           ` | `U+01EE67...U+01EE6A` | `U+01EE6C...U+01EE72` | `U+01EE74...U+01EE77` |
| `U+01EE79...U+01EE7C` | `U+01EE7E           ` | `U+01EE80...U+01EE89` | `U+01EE8B...U+01EE9B` |
| `U+01EEA1...U+01EEA3` | `U+01EEA5...U+01EEA9` | `U+01EEAB...U+01EEBB` | `U+01F100...U+01F10C` |
| `U+01FBF0...U+01FBF9` | `U+020000           ` | `U+02A6DF           ` | `U+02A700           ` |
| `U+02B739           ` | `U+02B740           ` | `U+02B81D           ` | `U+02B820           ` |
| `U+02CEA1           ` | `U+02CEB0           ` | `U+02EBE0           ` | `U+02F800...U+02FA1D` |
| `U+030000           ` | `U+03134A           ` | `U+031350           ` | `U+0323AF           ` |
| `U+0E0100...U+0E01EF` |                       |                       |                       |
