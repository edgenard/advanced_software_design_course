1.

a) The comparison to string constants is worrisome --- a typo in this or other code could be hard to detect, and what if the `student discount'' is renamed an `academic discount?'' Refactor the co\
de so that typos are a non-issue.

A:

```JAVA
public static final String CUSTOMER_TYPE_STUDENT = "student";
public static final String CUSTOMER_TYPE_EMPLOYEE = "employee";
```

b) {\tt customerTypeDiscount} and {\tt dayOfWeekDiscount} can contain arbitrary strings, even though they can only take a restricted set of values. What happens if the calling code passes in `Weekend'' as a day-of-week discount, or if the programmer adds a `veteran discount'' but forgets to update this code? Refactor the day-of-week and customer-type discounts so that they can only contain valid days of week or customer types.

A:

```JAVA
public class Customer {
public CustomerType getCustomerType() { ... }
}
public enum CustomerType { STUDENT("student"), EMPLOYEE("employee") }

public enum DayOfWeek { SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY }
// (Or use java.time.DayOfWeek)

```

c) This API allows you to apply a discount to an item that shouldn't get it. How would you modify the API to prevent that?

A:

Option 1: applyDiscount now only conditionally applies discount; does its own discount checking.

```JAVA
  private boolean doesDiscountApply(Customer c, Item item){
    // same as before
  }
  public double applyDiscount(Customer c, Item item, double price){
    return doesDiscountApply(c, item) ?
        price * (1 - discountPercent):
        price;
  }
```

Option 2: Use Tokens. doesDiscountApply returns an optional "DiscountApplier" object. Either make applyDiscount require a DiscountApplier as an argument, or move applyDiscount to be a method of DiscountApplier

```JAVA
public class Discount {
    public Optional<DiscountApplier> doesDiscountApply(Customer c, Item item);
    public double applyDiscount(DiscountApplier applier, double price)
}
public class DiscountApplier {}
```

d) It's intended that a discount can only be one of the three types. How would you redesign this code so that {\tt doesDiscountApply} contains no conditionals?

A:

Option 1:

```JAVA
public class CustomerTypeDiscount extends Discount { ... }
public class ItemNameDiscount extends Discount { ... }
```

Option 2:

```JAVA
public class Discount {
  private interface DiscountChecker {
    public boolean doesDiscountApply(Customer c, Item item);
  }

  private static class CustomerTypeDiscount implements DiscountChecker { ... }
  private static class ItemNameDiscount implements DiscountChecker { ... }
  private static class DayOfWeekDiscount implements DiscountChecker { ... }

  DiscountChecker discountChecker;

  public boolean doesDiscountApply(Customer c, Item item) {
      return discountChecker.doesDiscountApply(c, item);
  }

}
```

e) Bonus: With the current implementation, a day-of-week discount can't be tested without waiting until that day. How would you modify this program to make day-of-week discounts unit-testable?

A: Dependency-injection.

2. The Facebook codebase of 2010 is roughly organized into layers. The website layer displays user information in webpages, and provides end-user functionality like the Like button. The middle layer organizes data and provides operations on it, like like finding a user's top posts. The data layer organizes requests to the database. In the design above, all privacy checks happen in the web layer. How would you redesign the code so that all privacy checks happen at the data layer?

A: Thread a ViewerContext parameter through all methods.
