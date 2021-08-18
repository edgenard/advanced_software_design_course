# GIMP File Format Case Study

## Assumptions

> In images that use the indexed color model, GIMP does not support
partial transparency and interprets alpha values from 0 to 127 as
fully transparent and values from 128 to 255 as fully opaque. This
behavior _may_ change in future versions of GIMP.
TODO: has already changed?


1. Consider the assumption that indexed color mode does not allow partial transparency. How did this assumption spread into the file format? (Hint: It doesn't spread because there is special code to do so; it spreads because there is no code to block the assumption from spreading.)

    I think it spread because the alpha value  were allowed to be anything from 0 to 255 instead of restricting them to 0 or 255. If the data structure would have been more precise, I think it would been explicit that there is no partial transparency for files using the indexed color model.

2. Suppose you're a GIMP developer in 2014, and you'd like to add support for semitransparent pixels in indexed color mode. There are many old XCF files floating around which use arbitrary alpha values in indexed color mode, since they're all treated the same. You'd like new versions to display these images the same as old versions. What changes do you need to make to support this?

    I think I would have to add a version number to the file or something else that would identify it as a file that supported semitransparent pixels and have something in the code that branched on whether the file being read supported semitransparent pixels or not.

    I would also consider leaving indexed color mode alone and see if adding another property to the file might do the same thing. Old versions would not look for this new property. The new file reader could check if the old index color property is set and revert to the old way, and if it's not it render the file with transparent pixels

3. In truth, the GIMP developers did not alter the file format at all when they started supporting semitransparent index colors. Suppose you created an indexed-mode image with semitransparent pixels in a new version of GIMP, and opened it in 2.8.22 or older. What would you expect to happen?

    I would expect it to not either be fully transparent or fully opaque

4. What should the GIMP developers have done to prevent this assumption from spreading into the file format? How could they have prevented this problem in the first place?

    I think they should have restricted the alpha values to either be 0 or 255. I think that would have made it clear in the data structure that semitransparent pixels are not supported.



## Openness

1. Explain how to add a new property to the XCF file format, akin to the existing properties (PROP_COLORMAP, PROP_COMPRESSION, etc). Is XCF open in the set of properties?

    You can add a new property by adding it to the `property-list` field in the image data structure and you have to add a reader that can read that property. I think that seems open.

2. Pick two different properties. Explain how to add a new field to each. Are these properties open in the list of fields?

    I think to add properties you would have to go update the definition of that property. Since they are enums I think we are able to just add attributes to them. Old versions will just use the attributes and new versions can use the new attributes.


## Complexity Ratchets

1. For each of Format 1, Format 2, and Format 3 of the path property, write down the format as a product type.

    ```typescript
        type Format1 = {
            name: string
            linked: number //1 or 0
            state: byte
            closed: number
            np: number
            version: number
            points: Array<Points>
        }
        type Format2 = {
            name: string
            linked: number //1 or 0
            state: byte
            closed: number
            np: number
            version: number
            dummy: 1
            points: Array<Points>
        }

        type Format3 = {
            name: string
            linked: number //1 or 0
            state: byte
            closed: number
            np: number
            version: number
            dummy: 1
            tattoo: number | PROP_TATTOO
            points: Array<Points>
        }
    ```

3. Are any of these types a subtype of another? Think about the Liskov substitution principle.

    I think that Format2 is a subtype of Format1 and Format3 is a subtype of Format1 and Format2. I don't see why we can't use Format2 and Format3 anyplace we use Format1. However Format1 cannot be substituted for Format2 or Format3. It seems that the formats get more specific.

4. Write down a common super-type of all three formats. (There are multiple; give the most specific one you can.) If given a value of this super-type, what code would you need to write to destruct such a value?

    ```typescript
        type Format = {
            name: string
            link: number
            state: byte
            closed: number
            np: number
        }
    ```

5. Compare your answer in the previous question to the actual code that reads one of these paths. How could the GIMP authors have predicted the need for this if-statement from the initial design of the PROP_PATHS format?
6. Give a different way of expressing Formats 1, 2, and 3 such that Format 3 is a subtype of Format 2, and Format 2 is a subtype of Format 1. How would this enable pre-1999 versions of GIMP to read newer files? How would the xcf_load_old_path code differ in modern versions of GIMP?
