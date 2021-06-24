# Case Study: A Tale of Two Parsers

## Data Modeling

1. Look at JavaParser's PrimitiveType.Primitive enum. Express it as a sum type

    `public datatype PrimitiveType.Primitive = Boolean | Char | Byte | Short | Int | Long | Float | Double `

2. Consider JavaParser's PrimitiveType class. Express the valid values as an algebraic data type. It may help you to look at the getters and constructors.

    `public datatype PrimitiveInputs = void | PrimitiveType.Primitive | (PrimtiveType.Primitive,  NodeList<AnnotationExpr>)`

3. Repeat this exercise for JDT's PrimitiveType class. How does it differ from JavaParser?

    The JDT PrimitiveType class doesn't seem to allow it itself to be constructed, though it does have the same fields. It seems that the JDT version of
    `PrimitiveType` is more like a data type than a class. It seems the JavaParser version allows us to create an invalid `PrimitiveType` or maybe allows us to extend the
    `PrimitiveType`.

4. JavaParser's Type class has a getAnnotation() method, and so presumably also a corresponding annotations field. Consider pulling down this annotations field into each subtype. Show what this looks like in algebraic data type notation. What algebraic law are you using?

    ```java
       datatype Type = Intersection Annotations | PrimitiveType Annotations | ReferenceType Annotations | UnionType Annotations ...

    ```

    This is distributivity of multiplication across addition.

5. Look at JDT's Type class. Ignore all subclasses except ArrayType, UnionType, and AnnotatableType. Write the remainder of the Type class as an algebraic data type in terms of these subclasses. Repeat for AnnotatableType, considering only the subclasses PrimitiveType and SimpleType.

    ```java
    datatype Type = ArrayType Dimensions ElementType PropertyDescriptors | UnionType PropertyDescriptors Types | AnnotatableType Annotations

    datatype AnnotatableType = PrimitiveType Code SimpleProperDescriptor  | SimpleType ChildListPropertyDescriptor ChildPropertyDescriptor
    ```

6. Repeat for the JavaParser Type class, ignoring all subclasses except PrimitiveType, ReferenceType, UnionType, UnknownType, and VoidType. Repeat for the JavaParser ReferenceType class. (Ignore the ReferenceTypeMetaModel, which comes from later processing, and is not really part of the AST.)

    ```java
    datatype Type = PrimitiveType | ReferenceType | UnionType | UnknownType | VoidType

    datatype ReferenceType =
    ```

7. Show how to algebraically modify the two algebraic data types for the respective Type classes to be as similar as possible. Show your steps and name the algebraic laws used at each.


## Code follows data

Consider OffByOneOperation.java, which patches an expression by adding or subtracting one.

1. Look at the mutateIndex method, and consider the cases for PrefixExpression and PostfixExpression. What prevents the Genprog authors from merging both into one case?

    They have different requirements

2. Sketch what these cases would look like had Genprog 4 Java been built on Javaparser instead of the Eclipse JDT.
3. What changes would need to be made to the Eclipse JDT so that the authors of Genprog can merge these cases? What algebraic laws make this possible?
4. What would the authors of Genprog have to do in order to merge those cases without changing the Eclipse JDT?
