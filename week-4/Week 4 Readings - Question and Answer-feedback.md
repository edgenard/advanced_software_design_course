# Week 4 Readings - Question and Answer

#advanced-software-design-course/week-4

## [On the Criteria to be Used in Decomposing Systems Into Modules](http://citeseer.ist.psu.edu/viewdoc/download;jsessionid=EEA35F04282BD1CBB783C6973EA2C41A?doi=10.1.1.132.7232&rep=rep1&type=pdf) , David Parnas

A claim in the article is that, by decomposing the KWIC system into the second modular decomposition in the article, they could put any implementation of the pieces together to create a working system. Come up with a way of designing the pieces that still fits the decomposition, but so that they nonetheless don't work together. What lesson can we take from this?

I don't see how to design the pieces in such a way that

- Follow the "information hiding" modularization from the paper
- Meets the specifications for the system
- Do not work when put together.

<------------ Feedback -------------->
One example of it would be if the Circular Shift module could only store shifts. It still fits the specification as it was explicitly defined, but the system wouldn't work when put together.
<------------------------------------>

## [The Secret History of Information Hiding](https://www.dropbox.com/s/2j812i6347jbbrp/parnas_secret_history.pdf?dl=0) , David Parnas

Have you encountered a story like "The Napkin of Doom" in your own experience? What was the story, and how did it hurt?

I once worked on a grade book for a learning management system. The courses were authored in a separate system and that system produced a course outline in the form of a large json document. The course outline had information about what items in the course were gradable and some other information needed to make the grade book work. Anytime a change was made in the course outline produced by the course authoring system, we had to make sure it didn't break the grade book.

<------------ Feedback -------------->
Great example!
<------------------------------------>

## Research Corner: The Programmer's Apprentice, James Koppel

Suppose you wanted to extract out the part of the _foo_ method that computes the sum? How would its dataflow graph help you?

The dataflow graph shows what data you need and what you need to do to the data. In the `foo` example, it shows us that we need

- an array
- the length of the array
- A way of traversing the array
- A way to know when to stop traversing the array
- Something to keep accumulating the sum
- A way of calculating the sum

We can break this down like Parnas did into a "Master Control" module that coordinates other modules. The other modules could be something like "Array Storage" that has a getter for the values of the array(maybe something like `next` that returns each value and then finally something that indicates there are no more). The "Master control" then could pass those values to the "CalculateSum" module which return the current sum. "Master control" could also pass the array values to "CalculateMax" along with the current max, which always return the max value.

The above is just a rough sketch of how using a dataflow graph could help refactor the `foo` method. I think it could be possible to see this flow without creating dataflow graph but it would be a lot harder.

<------------ Feedback -------------->
The first part of the answer is good. The dataflow graph helps identify the data and operations involved which makes it easier to extract out the sum part.

Recall the following from the Parnas paper:

> We have tried to demonstrate by these examples that
> it is almost always incorrect to begin the decomposition
> of a system into modules on the basis of a flowchart.
> We propose instead that one begins with a list of
> difficult design decisions or design decisions which are
> likely to change. Each module is then designed to hide
> such a decision from the others.

The decomposition suggested above is much similar to the flowchart approach. As Parnas said, focus on the design decisions and decompose the system into modules from there.
<------------------------------------>
