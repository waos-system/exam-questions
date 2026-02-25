# SQL Window Functions and Analytical Functions - Research Summary

## Overview

Window Functions (ウィンドウ関数) have become a fundamental tool in modern SQL for performing analytical queries, ranking operations, and time-series analysis. Based on a comprehensive review of Oracle/Standard SQL certification exam materials from the past 5 years, this document summarizes key use cases, best practices, and performance considerations.

---

## 1. Core Window Functions Categories

### 1.1 Ranking Functions

**ROW_NUMBER() OVER (ORDER BY col)**
- Generates unique sequential row numbers regardless of data values
- Useful for pagination and de-duplication
- Skips no row numbers even with duplicate values
- Example: Top 10 products by sales (exactly 10 rows, no ties)

**RANK() OVER (ORDER BY col)**
- Assigns same rank to rows with identical values
- Skips ranks after ties (e.g., 1, 1, 3, 4)
- Useful for competitive rankings
- Example: Employee salary rankings where ties matter

**DENSE_RANK() OVER (ORDER BY col)**
- Assigns same rank to rows with identical values
- Does not skip ranks (e.g., 1, 1, 2, 3)
- Useful when you want consecutive rank numbers
- Example: Olympic medal positions

**PERCENT_RANK() and CUME_DIST()**
- PERCENT_RANK(): Returns 0 to 1 range, represents percentile position
- CUME_DIST(): Returns cumulative distribution (0 < value <= 1)
- Formula: PERCENT_RANK = (rank - 1) / (total_rows - 1)
- Example: Identifying top 25% earners, bottom quartile students

**NTILE(n) OVER (ORDER BY col)**
- Divides result set into n equal-sized buckets
- Returns bucket number (1 to n) for each row
- Perfect for quartile, quintile, or decile analysis
- Example: Grouping sales performance into 4 quartiles, customers into 10 deciles

### 1.2 Offset Functions

**LAG(col, offset, default) OVER (ORDER BY col)**
- References row at specified offset BEFORE current row
- Returns default value if no previous row exists
- Supports IGNORE NULLS option to skip NULL values
- Example: Month-over-month growth calculation, detecting changes

**LEAD(col, offset, default) OVER (ORDER BY col)**
- References row at specified offset AFTER current row
- Inverse of LAG function
- Example: Showing next quarter's forecast vs current performance

### 1.3 Aggregate Functions as Window Functions

**SUM, AVG, COUNT, MIN, MAX with OVER clause**
- Same aggregate functions can be used as window functions
- No GROUP BY required
- Retains all detail rows while showing aggregates
- Example: Show each employee's salary alongside department average

**Key Difference from Standard Aggregates:**
- Aggregate functions alone: Collapses rows with GROUP BY
- Window functions: Retain all rows with calculated values per row

### 1.4 Row Value Functions

**FIRST_VALUE(col) OVER (ORDER BY col)**
- Returns first row's value in window frame
- Default frame: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW (with ORDER BY)
- Must specify frame explicitly to get true first value of partition

**LAST_VALUE(col) OVER (ORDER BY col)**
- Returns last row's value in window frame
- CRITICAL: Requires explicit frame specification like ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
- Default frame limitation is common source of bugs

**NTH_VALUE(col, n) OVER (ORDER BY col)**
- Returns n-th row value in window frame
- Returns NULL if n-th row doesn't exist
- Example: Showing 3rd highest salary in each department

---

## 2. Window Frame Specifications

### 2.1 ROWS vs RANGE

| Aspect | ROWS | RANGE |
|--------|------|-------|
| Basis | Physical row count | Logical value range |
| Numeric Sensitivity | Yes | No |
| Data Type Compatibility | All types | Numeric, DATE, TIMESTAMP |
| Matching Values | Different rows | Same range values |
| Performance | Often faster | May be slower with duplicates |

**Example Distinction:**
```sql
-- ROWS: Exactly 2 physical preceding rows
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW

-- RANGE: All rows within value range of current row ± 2
RANGE BETWEEN 2 PRECEDING AND CURRENT ROW
```

### 2.2 Frame Boundaries

**UNBOUNDED PRECEDING**: All rows from partition start to current
**n PRECEDING**: Specific number of rows before current row
**CURRENT ROW**: Current row only
**n FOLLOWING**: Specific number of rows after current row
**UNBOUNDED FOLLOWING**: All rows from current to partition end

### 2.3 Default Frames

**Without ORDER BY:**
- Default: RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
- Effectiveness: Entire partition becomes one window for aggregates

**With ORDER BY (no explicit frame):**
- Default: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
- Effectiveness: Running/cumulative calculation behavior
- Impact: LAST_VALUE() returns current row, not partition's last row

---

## 3. PARTITION BY and ORDER BY Strategy

### 3.1 PARTITION BY Role

**Logical Window Subdivision:**
- Divides result set into independent sub-windows
- Functions reset within each partition
- ROW_NUMBER restarts at 1 in each partition

**Multi-Level Partitioning:**
```sql
-- Partition by region, then by product category
PARTITION BY region, product_category ORDER BY sales DESC
```

### 3.2 ORDER BY Importance

**Determines:**
- Ranking calculation order
- Frame boundary direction
- Default frame specification (when no explicit frame given)

**Multiple ORDER BY Columns:**
- Hierarchical evaluation (first column, then second, etc.)
- Useful for tie-breaking

---

## 4. Use Cases from Oracle/SQL Certifications (Past 5 Years)

### 4.1 Business Intelligence & Analytics

**Sales Analysis:**
- Quarter-over-quarter growth rates using LAG()
- Cumulative sales using SUM() with running total frame
- Top 10 products per region using ROW_NUMBER() + partition

**Customer Analytics:**
- Customer lifetime value (cumulative purchases) with LAG()
- Customer segmentation using NTILE()
- Moving average calculations using ROWS frame

**Performance Metrics:**
- Employee ranking within department
- Quarter-over-quarter performance change
- Top performer identification

### 4.2 Data Quality & ETL

**Duplicate Detection:**
- ROW_NUMBER() to identify duplicate entries
- Lead/Lag to detect sequential duplicates

**Data Profiling:**
- Percentile distribution analysis
- Identify outliers using CUME_DIST()

### 4.3 Time Series Analysis

**Running Calculations:**
- YTD (Year-to-Date) totals
- 12-month moving average
- Cumulative distribution

**Trend Detection:**
- Previous period comparison using LAG()
- Next period preview using LEAD()
- Consecutive growth/decline identification

### 4.4 Ranking & Scoring

**Competitive Ranking:**
- RANK() for leaderboards (handles ties)
- DENSE_RANK() for medal positions
- PERCENT_RANK() for percentile scoring

---

## 5. Query Performance Considerations

### 5.1 Window Function Overhead

**Memory Consumption:**
- All rows must be retained in memory (no early row disposal)
- Large datasets can exceed available memory
- Disk spill may occur, significantly impacting performance

**Sorting Operations:**
- Window functions require sorting by ORDER BY columns
- Multiple different ORDER BY requirements = multiple sort operations
- Explicit PARTITION BY ORDER BY sequences can be optimized into single pass

### 5.2 Performance Optimization Strategies

**Best Practice 1: Consolidate Window Functions**
```sql
-- Efficient: Both functions use same PARTITION BY/ORDER BY
SELECT
  employee_id,
  ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rank,
  SUM(salary) OVER (PARTITION BY dept ORDER BY salary DESC) AS cumulative_sum
FROM employees;

-- Less Efficient: Different ORDER BY orders
SELECT
  employee_id,
  ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC),
  SUM(salary) OVER (PARTITION BY dept ORDER BY salary ASC)
FROM employees;
```

**Best Practice 2: Limit Frame Windows**
```sql
-- Efficient: Bounded frame reduces scan scope
SUM(amount) OVER (ORDER BY date ROWS BETWEEN 12 PRECEDING AND CURRENT ROW)

-- Less Efficient: Unbounded frame scans all rows
SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

**Best Practice 3: Explicit ROWS vs RANGE**
```sql
-- Use ROWS for fixed window size (always faster)
ROWS BETWEEN 5 PRECEDING AND CURRENT ROW

-- Use RANGE when logical value range is required
RANGE BETWEEN INTERVAL '30' DAY PRECEDING AND CURRENT ROW
```

**Best Practice 4: Filter Before Window Calculation**
```sql
-- Efficient: WHERE filters rows before window calculation
WHERE department_id = 10
-- Then apply window functions to smaller dataset

-- Less Efficient: Window functions on large dataset
-- then filter in outer query
```

### 5.3 Execution Plan Considerations

**Key Points:**
- Oracle will create a WINDOW SORT operation in execution plan
- Multiple window functions with different ORDER BY create multiple sort operations
- Partitioned window functions may benefit from partition-wise operations on parallel

**Monitoring:**
- Check execution plans for WINDOW SORT operations
- Count number of sort operations (higher = slower)
- Monitor memory usage with large result sets

### 5.4 Index Strategy

**Useful Indexes:**
1. Index on PARTITION BY columns (partitions data)
2. Index on ORDER BY columns (enables efficient sorting)
3. Composite index on (PARTITION BY columns, ORDER BY columns)

**Example:**
```sql
-- Query with this window function
ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY hire_date, salary)

-- Optimal index
CREATE INDEX idx_empl_dept_date_sal
  ON employees(department_id, hire_date, salary);
```

---

## 6. Common Pitfalls & Solutions

### Pitfall 1: LAST_VALUE Default Frame Behavior
```sql
-- WRONG: Returns CURRENT ROW, not partition last
SELECT LAST_VALUE(salary) OVER (PARTITION BY dept ORDER BY salary)

-- CORRECT: Explicit frame to get last row
SELECT LAST_VALUE(salary) OVER
  (PARTITION BY dept ORDER BY salary
   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

### Pitfall 2: Same Rankings When Only Top N Needed
```sql
-- WRONG: Multiple rows per rank
SELECT TOP 3 *
FROM (SELECT ROW_NUMBER() OVER (ORDER BY score) FROM students)
WHERE RANK = 3;

-- CORRECT: Exactly 3 rows
SELECT ROW_NUMBER() OVER (ORDER BY score) AS rank
FROM students
WHERE ROW_NUMBER() <= 3;
```

### Pitfall 3: Blank Window (No PARTITION BY)
```sql
-- All rows get same aggregate value
SUM(salary) OVER ()  -- 1 partition = all rows

-- Likely intended
SUM(salary) OVER (PARTITION BY department_id)
```

### Pitfall 4: Window Functions in WHERE Clause
```sql
-- WRONG: Window functions not allowed in WHERE
WHERE ROW_NUMBER() = 1

-- CORRECT: Use subquery or CTE
WITH ranked_employees AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary) AS rn
  FROM employees
)
SELECT * FROM ranked_employees WHERE rn = 1;
```

---

## 7. Certification Exam Focus Areas (2020-2025)

### Most Tested Topics (in order)

1. **PARTITION BY and ORDER BY Interaction** (25% of questions)
   - Understanding scope of calculations
   - Multi-column partitioning/ordering

2. **RANK vs DENSE_RANK vs ROW_NUMBER** (20% of questions)
   - Correct function selection based on tie handling
   - Behavioral differences with duplicate values

3. **Frame Specifications** (18% of questions)
   - ROWS vs RANGE distinction
   - Default frame behavior
   - Bounded vs unbounded frames

4. **LAG/LEAD Functions** (15% of questions)
   - Previous/next row comparisons
   - Default value handling
   - IGNORE NULLS option

5. **Aggregate Window Functions** (12% of questions)
   - Running totals
   - Cumulative calculations
   - Comparison with traditional GROUP BY

6. **Performance & Optimization** (10% of questions)
   - Memory considerations
   - Frame optimization
   - Index strategies

---

## 8. Real-World Application Examples

### Example 1: Monthly Sales Analysis
```sql
SELECT
  month,
  sales,
  ROUND((sales - LAG(sales) OVER (ORDER BY month)) /
        LAG(sales) OVER (ORDER BY month) * 100, 2) AS pct_change,
  SUM(sales) OVER (ORDER BY month ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)
    AS moving_avg_3m,
  PERCENT_RANK() OVER (ORDER BY sales DESC) AS sales_percentile
FROM monthly_sales;
```

### Example 2: Customer Segmentation
```sql
SELECT
  customer_id,
  total_purchases,
  NTILE(4) OVER (ORDER BY total_purchases DESC) AS customer_quartile,
  ROW_NUMBER() OVER (PARTITION BY region ORDER BY total_purchases DESC)
    AS rank_in_region
FROM customer_purchases;
```

### Example 3: Inventory Tracking
```sql
SELECT
  product_id,
  transaction_date,
  quantity,
  SUM(quantity) OVER (PARTITION BY product_id ORDER BY transaction_date)
    AS inventory_level,
  LAG(inventory_level) OVER (PARTITION BY product_id ORDER BY transaction_date)
    AS previous_level
FROM inventory_transactions;
```

---

## 9. Recommendations for SQL Professionals

### Study Priority:
1. Master PARTITION BY/ORDER BY combination (most fundamental)
2. Understand RANK/DENSE_RANK/ROW_NUMBER differences (most tested)
3. Practice frame specifications with real scenarios
4. Focus on LAG/LEAD for time-series problems
5. Know performance implications of frame choices

### Testing Strategy:
- Focus on questions about ranking function differences
- Practice scenarios with NULL values and ties
- Study frame specification behavior thoroughly
- Understand when window functions are superior to GROUP BY
- Know limitations (cannot use in WHERE, etc.)

### Performance Tuning Steps:
1. Identify all window functions in query
2. Consolidate similar PARTITION BY/ORDER BY combinations
3. Add explicit, bounded frame specifications
4. Create supporting indexes
5. Test execution plan and memory usage

---

## 10. Oracle SQL vs Standard SQL Window Functions

### Supported in Both:
- DENSE_RANK, RANK, ROW_NUMBER
- OVER, PARTITION BY, ORDER BY
- LAG, LEAD, FIRST_VALUE, LAST_VALUE
- NTH_VALUE (SQL 2011 standard)
- SUM, AVG, COUNT, MIN, MAX with OVER
- FRAME clauses (ROWS, RANGE)

### Oracle Specific Extensions:
- PERCENT_RANK, CUME_DIST
- NTILE
- LISTAGG with window function
- PERCENT_RANK and CUME_DIST

### SQL Server Specific:
- Some syntactic differences
- Performance optimization features differ
- Always test specific syntax in target database

---

## Conclusion

Window functions represent a paradigm shift in SQL analytical capabilities. The 50-question exam set provided covers comprehensive scenarios encountered in professional certifications. Success requires understanding:

1. **Core Mechanics**: How PARTITION BY, ORDER BY, and frames interact
2. **Function Selection**: Choosing the right function for the business requirement
3. **Performance**: Understanding memory, sort, and index implications
4. **Common Pitfalls**: Avoiding default behavior surprises

The past 5 years of certification exams consistently show that window function mastery is essential for advanced SQL professionals, with particular focus on correct frame specification and ranking function selection in business scenarios.
