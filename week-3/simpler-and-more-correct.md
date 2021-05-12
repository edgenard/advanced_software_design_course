# Simpler and More Correct

## Exercise 1

```java
public class Discount {
  private String customerTypeDiscount;
  private String itemNameDiscount;
  private String dayOfWeekDiscount;

  private final double discountPercent;

  public boolean doesDiscountApply(Customer c, Item item) {
    if ( customerTypeDiscount != null) {
      if (customerTypeDiscount.equals("student")) return c.isStudent();
      else if (customerTypeDiscount.equals("employee")) return c.isEmployee();
    }

    if (itemNameDiscount != null) {
      return item.getName().equals(itemNameDiscount);
    }

    if (dayofWeekDiscount != null) {
      return DateUtils.getDayOfWeek().equals(dayOfWeekDiscount);
    }
    return false
  }

  public double applyDiscount(double price) {
    return price * (1 - discountPercent);
  }
}
```

1. The comparison to string constants is worrisome — a typo in this or other code could be hard to detect, and what if the “student discount” is renamed an “academic discount?” Refactor the code so that typos are a non-issue.

```java
public class Discount {
  private static final STUDENT_DISCOUNT = "student";
  private static final EMPLOYEE_DISCOUNT = "employee";
  private String customerTypeDiscount;
  private String itemNameDiscount;
  private String dayOfWeekDiscount;

  private final double discountPercent;

  public boolean doesDiscountApply(Customer c, Item item) {
    if ( customerTypeDiscount != null) {
      if (customerTypeDiscount.equals(STUDENT_DISCOUNT)) return c.isStudent();
      else if (customerTypeDiscount.equals(EMPLOYEE_DISCOUNT)) return c.isEmployee();
    }

    if (itemNameDiscount != null) {
      return item.getName().equals(itemNameDiscount);
    }

    if (dayofWeekDiscount != null) {
      return DateUtils.getDayOfWeek().equals(dayOfWeekDiscount);
    }
    return false
  }

  public double applyDiscount(double price) {
    return price * (1 - discountPercent);
  }
}
```

2. `customerTypeDiscount` and `dayOfWeekDiscount` can contain arbitrary strings, even though they can only take a restricted set of values. What happens if the calling code passes in “Week- end” as a day-of-week discount, or if the programmer adds a “veteran discount” but forgets to update this code? Refactor the day-of-week and customer-type discounts so that they can only contain valid days of week or customer types.

```java
enum Day {
  Monday,
  Tuesday,
  Wednesday,
  Thursday,
  Friday,
  Saturday,
  Sunday
}

enum CustomerType {
  Student, Employee
}

public class Discount {
  private CustomerType customerTypeDiscount;
  private String itemNameDiscount;
  private Day dayOfWeekDiscount;

  private final double discountPercent;

  public boolean doesDiscountApply(Customer c, Item item) {
    if ( customerTypeDiscount != null) {
      if (customerTypeDiscount.equals(CustomerType.Student)) return c.isStudent();
      else if (customerTypeDiscount.equals(CustomerType.Employee)) return c.isEmployee();
    }

    if (itemNameDiscount != null) {
      return item.getName().equals(itemNameDiscount);
    }

    if (dayofWeekDiscount != null) {
      return DateUtils.getDayOfWeek().equals(dayOfWeekDiscount.toString());
      // Not sure how DateUtils.getDayOfWeek() works could not find much documention on it, seems to be deprecreated.
      // Assuming it returns a string like "Monday", "Tuesday", etc
    }

    return false;
  }

  public double applyDiscount(double price) {
    return price * (1 - discountPercent);
  }
}
```

3. This API allows you to apply a discount to an item that shouldn’t get it. How would you modify the API to prevent that?

   I think the only way an item can get a discount that shouldn't get it is if the method `doesDiscountApply` is called with an item that is not eligible for a
   discount. So I would change the signature to take in `Customer` and a more specific type, `DiscountableItem` that would represent items are that eligible for a discount.


4. It’s intended that a discount can only be one of the three types. How would you redesign this code so that doesDiscountApply contains no conditionals?



5. Bonus: With the current implementation, a day-of-week discount can’t be tested without waiting until that day. How would you modify this program to make day-of-week discounts unit- testable?



## Exercise 2

The Facebook codebase of 2010 is roughly organized into layers. The website layer displays user information in webpages, and provides end-user functionality like the Like button. The middle layer organizes data and provides operations on it, like like finding a user’s top posts. The data layer organizes requests to the database. In the design above, all privacy checks happen in the web layer. How would you redesign the code so that all privacy checks happen at the data layer?

I think this could be done by writing queries that only return data that is viewable by the user. This would require the data to have some knowledge about who can view it.
I think this could be done with some kind of `has_many` relationship. For example, `photo.viewers` would be a list of who can view the photo.  Whatever the exact implementation
the strategy would be to model the data in such a way that who can view it and it what circumstances is built into the structure of the data.
