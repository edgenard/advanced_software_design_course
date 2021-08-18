Think about a datatype you've changed recently.

- Sketch out the type both before and after in algebraic datatype notation. How close is the new type to a subtype of the old type?
- What code changes did you have to make corresponding to the data type changes? How can these be predicted from the data type changes?
- What could you have done differently to make this change easier to implement?


I was working on a project to add annual promotions because we only supported monthly promotions.

Below is a slice of what the Promotion model looked like. These properties were mapped to database columns and the `subscription_duration_months` property was accessed all over the code base.

```
 interface Promotion {
   discount_percent: integer
   code: string
   subscription_duration_months: integer
 }
```

We decided that the `subscription_duration_months` column needed to be changed to something that was not tied to only monthly subscriptions(`billing_cycles`). In a Rails app usually each model is backed by a database table.
This model is then also used all over the codebase. This brings the specifics of a database table everywhere that model is used. So we had code in several places that referred to `subscription_duration_months`.
That code often assumed that the integer returned by `subscription_duration_months` represented months. Immediately it seemed we would have to do Shotgun Surgery, looking for every instance of the use of `subscription_duration_months` and
changing it to `billing_cycles`. We would also have to change the code to accommodate that the promotion could be an annual one instead of the monthly one it was assumed to be.

We ended up with something like this:

```
 interface Promotion {
   discount_percent: integer
   code: string
   billing_cycles: integer
 }
 ```

In hindsight I think the best way to do this would have been to hide the details of the database from the rest of the code, at least the column that was going to be changed. The changed `Promotion` interface could have looked something like this:

 ```
 interface Promotion {
   discount_percent: integer
   code: string
   private subscription_duration_month: integer
   billing_cycles(): integer // a method that hides "subscription_duration_month"
   duration(): Duration //This returns the length of time of the promotion either the number of months or the number of years
   duration_left(number_of_times_applied: integer): Duration // This returns the time left on the promotion for that user.

 }

```