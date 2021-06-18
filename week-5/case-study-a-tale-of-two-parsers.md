# Case Study: A Tale of Two Parsers

## Data Modeling

1. Look at JavaParser's PrimitiveType.Primitive enum. Express it as a sum type

    `public datatype PrimitiveType.Primitive = Boolean | Char | Byte | Short | Int | Long | Float | Double `

2. Consider Javaparser's PrimitiveType class. Express the valid values as an algebraic data type. It may help you to look at the getters and constructors.

    `

3. Repeat this exercise for JDT's PrimitiveType class. How does it differ from Javaparser?
4. Javaparser's Type class has a getAnnotation() method, and so presumably also a corresponding annotations field. Consider pulling down this annotations field into each subtype. Show what this looks like in algebraic data type notation. What algebraic law are you using?
5. Look at JDT's Type class. Ignore all subclasses except ArrayType, UnionType, and AnnotatableType. Write the remainder of the Type class as an algebraic data type in terms of these subclasses. Repeat for AnnotatableType, considering only the subclasses PrimitiveType and SimpleType.
6. Repeat for the Javaparser Type class, ignoring all subclasses except PrimitiveType, ReferenceType, UnionType, UnknownType, and VoidType. Repeat for the Javaparser ReferenceType class. (Ignore the ReferenceTypeMetaModel, which comes from later processing, and is not really part of the AST.)
7. Show how to algebraically modify the two algebraic data types for the respective Type classes to be as similar as possible. Show your steps and name the algebraic laws used at each.
