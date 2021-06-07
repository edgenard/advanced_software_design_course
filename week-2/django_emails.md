1. Compare the write_message methods of the console-based and file-based backends.
   There is hidden coupling between them. What is the hidden coupling?
   What changes does this hidden coupling inhibit? How would you refactor them to eliminate it.

A: Assuming you want E-mails to be sent consistently, the ('-' \* 79) separator is shared between them.
In fact, the code between them is the same, but acts on different encodings (byte strings vs. ASCII strings).
A solution is to actually unify both implementations of write_message into the superclass, but abstract over the encoding.
Can put this in send_messages, or move part of write_message to the superclass (console backend), or a shared format-E-mail method.
There are also many other options.

2. The send_messages methods of both the SMTP-based and console-based (and file-based, by inheritance)
   backends have a common notion of failing silently according to an option.

2.1) What is the essence of the "fail-silently" pattern? In other words,
if I gave code where all identifiers were obfuscated, how would you identify code that implemented the "fail-silently" feature?
Give your answer either as a very specific description of data- and control-flow to look for, or as a code skeleton.

A: "Failing silently" is defined by wrapping code in a try/catch handler that conditionally ignores exceptions.
It's a shared fragment of the control-flow graph.

```
try:
  ...
except (kinds of exception) as e:
  if not self.fail_silently:
    raise e
```

2.2) What are the design decisions which are the same between the two backend's implementation of fail-silently,
and how might a change to these decisions affect both implementations? Think about other policies for how the
application should handle exceptions other than "fail at the top-level immediately for all exceptions"
and "silently drop all exceptions."

A:
The design decisions affecting both backends can be described as follows:
During the process of sending messages (open connection, send messages, close connection) errors will be dealt with in one of two ways:
-Any of them will make the process of sending messages stop right when the error happens.
-All errors will be ignored and the application will continue to try sending the messages.

Similar to question 1 of this case study, if there's a change to the decision of what error handling policies should exist,
both backend implementations will have to change.

Some examples of other policies would be:
-Always fail in case of specific errors.
-Always ignore certain errors.
-Retry operation when specific errors happen.

2.3) Sketch how to refactor the code to eliminate this hidden coupling.
A successful solution should give code for "failing silently" that can be used in contexts unrelated to E-mail.
(Hint: Use Python's with statement)

To refactor out a common subexpression or sequence of statements by refactoring to a function call or shared constant,
it's possible to refactor this pattern as a higher order function, which takes the "..." body as a function parameter.
In Python, there is special syntax for doing this: you can use a with-statement instead of calling a higher-order function.

with error_handling_policy():
self.connection.sendmail(from_email, recipients, message.as_bytes(linesep='\r\n'))

The return type of error_handling_policy() is a Python context manager, i.e.: something with **enter** and **exit** methods.

The equivalent Java code would be this:

```JAVA
this.errorHandlingPolicy.doFailableAction(() -> {
this.connection.sendmail(...);
});
```

where doFailableAction has many possible implementations.

Below is one example of a possible refactor for this exercise using Python.

Create a class that implements the concept of fail_silently and create an instance of that class on BaseEmailBackend's constructor.

```Python
  class FailControl:
    def __init__(self, fail_silently):
      self.fail_silently = self.fail_silently
    def __enter__(self):
      pass
    def __exit__(self, type, value, traceback):
      return fail_silently

  class BaseEmailBackend:
    def __init__(self, fail_control=FailControl(fail_silently), **kwargs):
          self.fail_control = fail_control
```

Refactor the existing code that implements the fail_silently concept to use the instance of FailControl.
Example of refactoring for one of the methods.

```Python
# refactor of method _send on the SMTP backend
def _send(self, email_message):
  """A helper method that does the actual sending."""
  if not email_message.recipients():
    return False
  encoding = email_message.encoding or settings.DEFAULT_CHARSET
  from_email = sanitize_address(email_message.from_email, encoding)
  recipients = [sanitize_address(addr, encoding) for addr in email_message.recipients()]
  message = email_message.message()
  with self.fail_control:
    self.connection.sendmail(from_email, recipients, message.as_bytes(linesep='\r\n'))
    return True
  return False
```

3. The **init** method of the file-based backend is complicated because of the impedance mismatch
   between the file path argument it accepts and the actual requirements on files.

   3.1) What are the concrete restrictions it is placing on file paths? What are the underlying design decisions behind these restrictions?

Concrete restrictions:

- File path must be a string
- If file path points to an existing resource it must be a directory
- The directory pointed by the file path must be writable

Examples of design decisions that contributed to the origin of code that checks the above restrictions:

- Emails written by the file backend will be written to a directory
- Users of the file backend should be able to specify which directory the emails should be written to.

  3.2) What changes to the system's overall design or assumptions may change this code?

Most changes that would somehow impact the design decisions mention in 3.1 would cause the code to change. For example:

- All emails should be written to a single .txt file.
- Emails will be stored in N different directories depending on their content.

Note how in the code there are a lot of assumptions about how permissive the OS in which the code will run is.
If the server starts running on an OS with a more restrictive permissions system, the code will have to change.

3.3) Sketch how to refactor this method to embed the design decisions identified in 3.1 directly into the code.

Replace the file_path with an instance of a new class called ExtantWritableDirectory.
An instance of this class would perform all the validations that are currently performed on the filebased backend constructor.

        ```Python
        class ExtantWritableDirectory:
          def __init__ (self, file_path):
            # code from filebased backend constructor
            if file_path is not None:
                self.file_path = file_path
            else:
                self.file_path = getattr(settings, 'EMAIL_FILE_PATH', None)
            self.file_path = os.path.abspath(self.file_path)
            try:
                os.makedirs(self.file_path, exist_ok=True)
            except FileExistsError:
                raise ImproperlyConfigured(
                    'Path for saving email messages exists, but is not a directory: %s' % self.file_path
                )
            except OSError as err:
                raise ImproperlyConfigured(
                    'Could not create directory for saving email messages: %s (%s)' % (self.file_path, err)
                )
            if not os.access(self.file_path, os.W_OK):
                raise ImproperlyConfigured('Could not write to directory: %s' % self.file_path)

          def get_path(self):
            return self.file_path
        ```

        Refactor the filebased backend to use ExtantWritableDirectory

        ```Python
        def __init__(self, *args, destination_directory=setting.get_email_directory(), **kwargs):
         self._fname = None
         self.destination_directory = destination_directory
         # Finally, call super().
         # Since we're using the console-based backend as a base,
         # force the stream to be None, so we don't default to stdout
         kwargs['stream'] = None
           super().__init__(*args, **kwargs)

        def _get_filename(self):
         """Return a unique file name."""
         if self._fname is None:
           timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
           fname = "%s-%s.log" % (timestamp, abs(id(self)))
           self._fname = os.path.join(self.destination_directory.get_path(), fname)
         return self._fname
        ```

Note that before the refactoring a programmer could only rely on the fact that the given file path was an existing and writable directory in the code that runs after all the checks in `__init__` and in the methods of the backend. By moving those checks to `ExtantWritableDirectory`
those facts become invariants of the class and can be used in many places aside from just the backend. And furthermore, if the directory is
generated not from a string but from somewhere else, e.g.: a routine that creates a new writeable directory, then these checks may not need to be performed at all

The refactor also makes explicit the design decision of allowing users of file backend to specify the target directory.
Also note how it encapsulates assumptions about the OS the server is running on. If those assumptions change, there's no longer risk of introducing
new bugs on the file backend while adjusting code related to directories.

4. Look at the **init** and message methods of EmailMessage. Notice the different representations and handling of different E-mail headers such as from, bcc, to.

4.1) Use decision tables to explain how the different headers are treated.
Create two decision tables: one to explain how a header is handled when an initial value is given in the constructor, and one to explain when none is given.

When headers are given an initial value in the constructor:

| Header name(s)       | is tuple or list ? | is in headers parameter? | Action                                           |
| -------------------- | ------------------ | ------------------------ | ------------------------------------------------ |
| "to","cc","Reply-to" | T                  | T                        | use value in "headers" parameter                 |
| "to","cc","Reply-to" | T                  | F                        | concat values given in header specific parameter |
| "to","cc","Reply-to" | F                  | -                        | Raise exception                                  |
| "bcc"                | T                  | -                        | use "bcc" parameter value                        |
| "bcc"                | F                  | -                        | Raise exception                                  |
| "From"               | -                  | T                        | use value in "headers" parameter                 |
| "From"               | -                  | F                        | use "From" parameter value                       |
| "subject"            | -                  | -                        | use "subject" parameter value                    |
| others               | -                  | T                        | use value in "headers" parameter                 |
| others               | -                  | F                        | Header won't be set                              |

When headers aren't explicitly given a value in a constructor parameter or simply there isn't a parameter for them (e.g date and Message-ID):

| Header name(s)             | is in headers parameter | Action                           |
| -------------------------- | ----------------------- | -------------------------------- |
| "to","cc","reply-to","bcc" | -                       | use value []                     |
| "From"                     | T                       | use value in "headers" parameter |
| "From"                     | F                       | use value in settings            |
| "subject"                  | -                       | use ''                           |
| "date"                     | T                       | use value in "headers" parameter |
| "date"                     | F                       | date of header creation          |
| "Message-ID"               | T                       | use value in "headers" parameter |
| "Message-ID"               | F                       | Generated id based on DNS name   |
| others                     | T                       | use value in "headers" parameter |
| others                     | F                       | Header won't be set              |

4.2) Suppose a new standard came out. It says that every E-mail must have a "Reply-to" header. It also allows all recipients to be tagged with a reason
(e.g.: "CC: thanks:intro-er@example.com, keeping-in-the-loop:my-boss@example.com"). What changes would this require in the code?

For reply-to: Add validation to **init**. and remove the call to `_set_list_header_if_not_empty` otherwise reply-to might be set with invalid values from the headers parameter.

For CC-reason: CC will need a new data structure that can hold both an email and a reason. The email should be mandatory and the reason optional.
The code that verifies that the given CC is valid, will have to change to accommodate the new data structure.

4.3) Explain the design of the abstract concept of different kinds of headers,
i.e.: how would you explain what headers are, what variations there are, and how they work to someone who had never seen them before?
How are these ideas expressed in the code? How does this make the code complicated?

Headers are designed to convey information to the system handling the email.
There can be different types (e.g. list vs string), and they can be mandatory or not.
Ultimately they all become a mapping of string key to string value inside the message.

For a detailed explanation of the abstract concept of headers give a quick scan to the [Internet Message Format (RFC)](https://datatracker.ietf.org/doc/html/rfc5322). The description of headers starts on page 7, and after that, there are sections dedicated to each kind of header (E.g Destination address fields, identification fields, ...)

The code expresses these as primitive types and identifies them either as a passed in argument to the constructor,
or the name of the key.
This requires a lot of special casing for different types (e.g. the repeated list/tuple checks for to, cc, bcc, etc.).
Further some of the headers are kept as k/v pairs inside `self.extra_headers` whereas others are stored as properties
on the `EmailMessage` itself.
Both of these complicate the code because you need to do a lot of reflection to see what type you have,
as well as look for properties in multiple places, knowing which can exist on the message itself and which cannot,
which are required and which are not, etc..

Answer of Mitchell Rivet: From wikipedia: "Each message has exactly one header, which is structured into fields.
Each field has a name and a value".
There is a separator (":") between header and value. "From" and "Date" are required for a valid header.
These basic formatting rules are expressed in code line by line, and are very much "dark knowledge".

If I know nothing about email headers, these implementation requirements are not clear to me (or at least quickly accessible)
through this code. It would be much quicker to grasp if we abstracted these

4.4) Sketch how to refactor this code based on the abstract design of headers.

Two majors families of solutions are to have a type for types of E-mail headers, or to have a type for E-mail headers.
In the former, the EmailMessage class maintains a list of "header schema descriptions,"
capable of inspecting an unstructured key/value list and extracting relevant header information.
In the latter, the caller is responsible for passing in headers as structured data.

Here is an example from a student who implemented the first approach: https://gist.github.com/gabrielgiordano/9ef3f93927a6ece5f59c7d1b0425f7a1.
The main detail is the FIELDS data structure on line 52; the others are less important.

5. Find one more instance of a design-level concept which is only indirectly expressed in this code, and explain how to refactor it.
   Code smells that may help you find examples include: if-statements, the use of base types such as bool or string to represent
   more complicated concepts, and methods that have multiple return types.

A: One example: E-mail attachments. As one student writes:

    The design concept of an email attachment is not well-embedded in this code,
    and consequently there are many rough edges where the code that does handle it deals with multiple types and subtypes,
    takes instances of attachment representations or primitive types it builds into attachments, etc..
    Many methods are dealing with far too many different input types. This is exemplified even in the comments, such as:

    > Convert the content, mimetype pair into a MIME attachment object.
    If the mimetype is message/rfc822, content may be an email.Message or EmailMessage object, as well as a str.

    The central interface everything is operating on is a the `EmailMessage`'s .attach method, which takes a filename,
    content and mimetype, and itself will handle a lot of variants, ultimately just doing:

```python
 # If MIMEBase: no content/no mimetype
 self.attachments.append(filename)
 # Otherwise
 self.attachments.append((filename, content, mimetype))
```

I would therefore refactor this by expressing the fact that there are multiple types of attachments,
and they can either have a filename and no content or mimetype, or they can have a filename, content and mimetype.
Thus we can create an attachment type, and then having various factory methods to create them by passing in filename and optionally
(content + mimetype). This way you wouldn't have metho ds that are force to handle all of the optionals,
rather you would create specific types of `Attachment`s based on what you were intending to provide.

We could represent mimetype as its own ADT as well, and have methods on it to `guess_type` etc.,
from the filename, so that our `Attachment` class is always provided with one if it exists.

More examples: forbid_multi_line_headers, HTML vs. plaintext E-mails

6. Bonus (optional): There are also at least two violations of the representable/valid principle (next week's lesson) in this code
   (at least one where it is possible to represent invalid states, and at least one where there are multiple states of EmailMessage
   that correspond to the same E-mail). Find them. How would you eliminate them? How would this simplify the code?

A:
Instance 1:

     if self.use_ssl and self.use_tls:
         raise ValueError(
             "EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive, so only set "
             "one of those settings to True.")

Instance 2:

     Some headers can be specified both as a property of the Message object, and in the extra_headers field.
     E.g.: the "from" field. Additionally, it is possible to add multiple copies of the same header,
     because E-mail headers are case insensitive, but the extra_headers map is case-sensitive.

Related:

    When we pass the To, Cc or Reply-To header into the header variable in the constructor,
    and don't pass a value in the to, cc, reply_to variables in the constructor (or pass a list with the empty string),
    this would cause the _set_list_header_if_not_empty method to leave these headers empty in the message even though we passed
    the values in the constructor.

```

```
