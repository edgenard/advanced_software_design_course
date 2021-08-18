# Questions from Readings


## Designing Software for Ease of Extension and Contraction

__Review "The criteria to be used in allowing one program to use another" on page 132. Think about a system whose design you're familiar with. Does its pattern of uses follow these criteria?__

I work mostly in Rails. I notice that ActiveRecord makes accessing the database very easy. However what usually happens is that we mix in the use of that data into the same class that accesses the data.
So we have several levels of the "uses" hierarchy mixed into one object. This is common in the Rails world.



## Martian Headsets

__How might the ideas in this article apply to individual functions in a single file?__

The situation described in the article is the opposite of the Robust code through restricted API exercise.
If we are lax about the parameters to a function it leads so a lot of checking of parameters  in order to know how
to handle them. If the function is written is such a way as to be strict in what it accepts, the function has to do a lot
less work.


## Gay Marriage: The Database Engineering Perspective

__When you see each DB variant, pause to think about its flaws, and what changes to the DB schema would be easy vs. hard.__

I think the article mentions what situation each variant could not handle until the schema becomes a graph.