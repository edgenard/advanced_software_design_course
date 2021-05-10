# Django Case Study

## Questions

1. Compare the write_message methods of the console-based and file-based backends.
There is hidden coupling between them. What is the hidden coupling? What changes does this hidden coupling inhibit?
How would you refactor them to eliminate it?

It seems that the messages is not in a form that it can just be written to the console or written to a file as is. The `message` needs to be transformed into bytes. While the for the console the message data needs to be decoded by the character or use the default of `utf-8` It also seems that the message needs to be followed by a `\n` then 79 dashes then another `\n`.

I would refactor this by introducing a method or object that formats the message with a parameter that controls whether or not it tries to decode the message by character set.



2. The send_messages methods of both the SMTP-based and console-based (and file-based, by inheritance) backends have a common notion of failing silently according to an option.
    1. What is the essence of the "fail-silently" pattern? In other words, if I gave code where all identifiers were obfuscated, how would you identify code that implemented the "fail-silently" feature? Give your answer either as a very specific description of data- and control-flow to look for, or as a code skeleton.

   The essence of the fail silently pattern is to catch exceptions, sometimes specific ones, and only raise if a certain condition is met.


    2. What are the design decisions which are the same between the two backend's implementation of fail-silently, and how might a change to these decisions affect both implementations? Think about other policies for how the application should handle exceptions other than "fail at the top-level immediately for all exceptions" and "silently drop all exceptions."

    **I'm not sure what those decisions are or other ways of dealing with exceptions.**


    3. Sketch how to refactor the code to eliminate this hidden coupling. A successful solution should give code for "failing silently" that can be used in contexts unrelated to E-mail. (Hint: Use Python's with statement)

    **Without being able to answer the previous question, I don't think I can answer this one**


3. The __init__ method of the file-based backend is complicated because of the impedance mismatch between the file path argument it accepts and the actual requirements on files.
   1. What are the concrete restrictions it is placing on file paths? What are the underlying design decisions behind these restrictions?
   The concrete restrictions are that `file_path` must be a string, point to a directory, and writable. I can't tell what underlying design decisions behind the restrictions other than that the choice to that the file-based backend will write files to directory.


   2. What changes to the system's overall design or assumptions may change this code?

      The only thing I can think of is the ability to create directories and files in the underlying operating systeam and the rules around that for different operating systems.

   3. Sketch how to refactor this method to embed the design decisions identified in 3.1 directly into the code.

    The best refactoring I can come up with is extract all of the logic about `file_path` into it's own object. It can handle the rules and configuration for a file path. If those rules change than the `__init__` method doesn't have to change.

    ```python
      def __init__(self, *args, file_path=None, **kwargs):
        self.file_path = FilePathMaker(file_path).path
        kwargs['stream'] = None
        super().__init__(*args, **kwargs)
    ```

4. Look at the __init__ and message methods of EmailMessage. Notice the different representations and handling of different E-mail headers such as from, bcc, to.
   1. Use decision tables to explain how the different headers are treated. Create two decision tables: one to explain how a header is handled when an initial value is given in the constructor, and one to explain when none is given.

    When email headers are passed in:

    | Header   | is a string? | output                                        |
    |----------|--------------|-----------------------------------------------|
    | to       | Yes          | Turn into List                                |
    | to       | No           | Raise error saying it must be a list or tuple |
    | cc       | Yes          | Turn into list                                |
    | cc       | No           | Raise error saying it must be a list or tuple |
    | bcc      | Yes          | Turn into list                                |
    | bcc      | No           | Raise error saying it must be a list or tuple |
    | reply_to | Yes          | Turn into list                                |
    | reply_to | No           | Raise error saying it must be a list or tuple |

    When email headers are not passed in:

    | Header   | output     |
    |----------|------------|
    | to       | empty list |
    | cc       | empty list |
    | bcc      | empty list |
    | reply_to | empty list |


   2. Suppose a new standard came out. It says that every E-mail must have a "Reply-to" header. It also allows all recipients to be tagged with a reason (e.g.: "CC: thanks:intro-er@example.com, keeping-in-the-loop:my-boss@example.com"). What changes would this require in the code?

    To satisfy the standard the check that `reply-to` is a string would also have to check that is exists and raise an error if it does not.

    The tagging can be ignored unless there's some requirement that changes something about the messsage. It's possible that only the recipients email client will use that information. If the tags change something like the header, or body of the message than I think lines like:

    ```python
     if to:
            if isinstance(to, str):
                raise TypeError('"to" argument must be a list or tuple')
            self.to = list(to)
    ```

    become something like

    ```python
     if to:
            if isinstance(to, str):
                raise TypeError('"to" argument must be a list or tuple')
            self.to = Recipient(to) # Recipient is some kind of data structure that deals with tags and whatever other kind of operations may need to be done with Recipients
    ```

   3. Explain the design of the abstract concept of different kinds of headers, i.e.: how would you explain what headers are, what variations there are, and how they work to someone who had never seen them before? How are these ideas expressed in the code? How does this make the code complicated?

   The best I can tell about headers is that the are part of the message. Only a few seem to be required, "Subject", "From", "Date", and "Message-ID". The message seems to be a key/value data structure where the headers and their values make up some of the keys.


   4. Sketch how to refactor this code based on the abstract design of headers.
      I'm not sure how I would refactor this.


5. Find one more instance of a design-level concept which is only indirectly expressed in the Django E-mail code, and explain how to refactor it. Code smells that may help you find examples include: if-statements, the use of base types such as bool or string to represent more complicated concepts, and methods that have multiple return types.

 **I'm going to skip this because I would like feedback on what I've done so far.**


6. Bonus (optional): There are also at least two violations of the representable/valid principle (next week's lesson) in this code (at least one where it is possible to represent invalid states, and at least one where there are multiple states of EmailMessage that correspond to the same E-mail). Find them. How would you eliminate them? How would this simplify the code?

Also very interested in this answer.