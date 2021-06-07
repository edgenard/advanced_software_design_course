# Django Case Study

## Questions

1. Compare the write_message methods of the console-based and file-based backends.
   There is hidden coupling between them. What is the hidden coupling? What changes does this hidden coupling inhibit?
   How would you refactor them to eliminate it?

It seems that the messages is not in a form that it can just be written to the console or written to a file as is. The `message` needs to be transformed into bytes. While the for the console the message data needs to be decoded by the character or use the default of `utf-8` It also seems that the message needs to be followed by a `\n` then 79 dashes then another `\n`.

I would refactor this by introducing a method or object that formats the message with a parameter that controls whether or not it tries to decode the message by character set.

<------------ Feedback -------------->
Correct
<------------------------------------>

2.  The send_messages methods of both the SMTP-based and console-based (and file-based, by inheritance) backends have a common notion of failing silently according to an option.

    1. What is the essence of the "fail-silently" pattern? In other words, if I gave code where all identifiers were obfuscated, how would you identify code that implemented the "fail-silently" feature? Give your answer either as a very specific description of data- and control-flow to look for, or as a code skeleton.

    The essence of the fail silently pattern is to catch exceptions, sometimes specific ones, and only raise if a certain condition is met.

    <------------ Feedback -------------->
    Correct
    <------------------------------------>

    2. What are the design decisions which are the same between the two backend's implementation of fail-silently, and how might a change to these decisions affect both implementations? Think about other policies for how the application should handle exceptions other than "fail at the top-level immediately for all exceptions" and "silently drop all exceptions."

    **I'm not sure what those decisions are or other ways of dealing with exceptions.**

    <------------ Feedback -------------->
    One thing to keep in mind about design decisions is that they are what give origin to a particular unit of code. With that in mind its possible to look at a piece of code and have a general idea of what the programmers were trying to accomplish.

    In this particular case, the code under analysis is code that is responsible for determining how exceptions are dealt with. And the way the code deals with exceptions is by either silencing all of them or failing as soon as something goes wrong.

    This behavior of all or nothing when dealing with exceptions hints towards what were the intentions of the programmers. In this case, it would be fair to say that the underlying design decision was something along the lines of:

    During the process of sending messages (open connection, send messages, close connection) errors will be dealt with in one of two ways:

    - Any of them will make the process of sending messages stop right when the error happens.
    - All errors will be ignored and the application will continue to try sending the messages.

    Other policies that might make sense to implement would be:

    - Always fail in case of specific errors.
    - Always ignore certain errors.

    <------------------------------------>

    3. Sketch how to refactor the code to eliminate this hidden coupling. A successful solution should give code for "failing silently" that can be used in contexts unrelated to E-mail. (Hint: Use Python's with statement)

    **Without being able to answer the previous question, I don't think I can answer this one**

    <------------ Feedback -------------->
    Please check the official solutions and let us know if there are any questions.
    <------------------------------------>

3.  The **init** method of the file-based backend is complicated because of the impedance mismatch between the file path argument it accepts and the actual requirements on files.

    1. What are the concrete restrictions it is placing on file paths? What are the underlying design decisions behind these restrictions?
       The concrete restrictions are that `file_path` must be a string, point to a directory, and writable. I can't tell what underlying design decisions behind the restrictions other than that the choice to that the file-based backend will write files to directory.

       <------------ Feedback -------------->
       Good job identifying a possible design decision!

       Note that it doesn't need to point to a directory necessarily. If it points to a file it has to be a directory, but if the "directory" doesn't exist it will be created. The other restrictions are correct.
       <------------------------------------>

    2. What changes to the system's overall design or assumptions may change this code?

       The only thing I can think of is the ability to create directories and files in the underlying operating systeam and the rules around that for different operating systems.

    <------------ Feedback -------------->
    Good job identifying the assumptions the system makes towards the OS.

    One example of a change to the design that would impact the code is that emails should be written to a single .txt file. This is a design decision that undos the decision mentioned in the previous exercise, so the code will have to change.
    <------------------------------------>

    3. Sketch how to refactor this method to embed the design decisions identified in 3.1 directly into the code.

    The best refactoring I can come up with is extract all of the logic about `file_path` into it's own object. It can handle the rules and configuration for a file path. If those rules change than the `__init__` method doesn't have to change.

    ```python
      def __init__(self, *args, file_path=None, **kwargs):
        self.file_path = FilePathMaker(file_path).path
        kwargs['stream'] = None
        super().__init__(*args, **kwargs)
    ```

    <------------ Feedback -------------->
    Great job! The overall idea of encapsulating the checks in a type is the core part of this refactoring, as it makes the check an invariant of that type and any code that uses it can rely on that invariant.

    I'd suggest refactoring `__init__` to receive a `FilePathMaker` instead of receiving a string. This has the advantage that if a `FilePathMaker` is generated not from a string but from somewhere else, `__init__` doesn't have to change. It also rids `__init__` of having to deal with the possibility of strings with invalid `file_paths`.
    <------------------------------------>

4.  Look at the **init** and message methods of EmailMessage. Notice the different representations and handling of different E-mail headers such as from, bcc, to.

    1. Use decision tables to explain how the different headers are treated. Create two decision tables: one to explain how a header is handled when an initial value is given in the constructor, and one to explain when none is given.

    When email headers are passed in:

    | Header   | is a string? | output                                        |
    | -------- | ------------ | --------------------------------------------- |
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
    | -------- | ---------- |
    | to       | empty list |
    | cc       | empty list |
    | bcc      | empty list |
    | reply_to | empty list |

    <------------ Feedback -------------->
    Something to keep in mind about tools such as decision tables is that they're used to help people reason more clearly about the intended behavior so that the implementation becomes easier. Therefore it's important for the decision table to be developed until the point that just by looking at it there's a clear idea of the overall behavior. In the case of this solutions, it is lacking information on what to do with headers such as "date" or "Message-ID", and also what should happen if the headers are also in the headers parameter.
    <------------------------------------>

    2. Suppose a new standard came out. It says that every E-mail must have a "Reply-to" header. It also allows all recipients to be tagged with a reason (e.g.: "CC: thanks:intro-er@example.com, keeping-in-the-loop:my-boss@example.com"). What changes would this require in the code?

    To satisfy the standard the check that `reply-to` is a string would also have to check that is exists and raise an error if it does not.

    <------------ Feedback -------------->
    Correct. The class to `_set_list_header_if_not_empty` will also have to be removed, otherwise `reply-to` might be overriden with an invalid value.
    <------------------------------------>

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

    <------------ Feedback -------------->
    Seems to have been some confusion here between the CC header and to header. But the overall idea of the introduction of a new data structure is correct.
    <------------------------------------>

    3. Explain the design of the abstract concept of different kinds of headers, i.e.: how would you explain what headers are, what variations there are, and how they work to someone who had never seen them before? How are these ideas expressed in the code? How does this make the code complicated?

    The best I can tell about headers is that the are part of the message. Only a few seem to be required, "Subject", "From", "Date", and "Message-ID". The message seems to be a key/value data structure where the headers and their values make up some of the keys.

    <------------ Feedback -------------->
    From the overall description of the concept of headers its missing the idea that headers are designed to convey information to the system handling the email, and also that they have different types.

    Check the official solutions for a description of how the way these ideas are expressed in the code makes it complicated.
    <------------------------------------>

    4. Sketch how to refactor this code based on the abstract design of headers.
       I'm not sure how I would refactor this.

    <------------ Feedback -------------->
    One of the core lessons of this module is that by making the code reflect the ideas that gave origin to it we can increase its quality.

    This lesson has an interesting implication, which is that if there's no idea of the design of the system, them there's no goal to refactor it towards.

    So when looking at code that needs to be refactored but the way to do it is not obvious, using techniques that help make the intended behavior of the code clear help. Techniques such as the plain english test (as shown in the lecture) or the decision table are really useful here. Try to use them to the point where just by looking at what they've produced is clear what the behavior should be. After that, the direction in which to take the refactor should become much clear.

    Please check the official solutions and pay special attention to how the refactoring of this exercise maps the answer to the previous one.
    Please let us know if there still are any questions after reading the solutions.
    <------------------------------------>

5.  Find one more instance of a design-level concept which is only indirectly expressed in the Django E-mail code, and explain how to refactor it. Code smells that may help you find examples include: if-statements, the use of base types such as bool or string to represent more complicated concepts, and methods that have multiple return types.

**I'm going to skip this because I would like feedback on what I've done so far.**

<------------ Feedback -------------->
Check the official solutions and let us know if there are any questions.
<------------------------------------>

6. Bonus (optional): There are also at least two violations of the representable/valid principle (next week's lesson) in this code (at least one where it is possible to represent invalid states, and at least one where there are multiple states of EmailMessage that correspond to the same E-mail). Find them. How would you eliminate them? How would this simplify the code?

Also very interested in this answer.

<------------ Feedback -------------->
Check the official solutions and let us know if there are any questions.
<------------------------------------>
