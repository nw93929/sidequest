Project Milestone 2: Plan and Build Your App with Streamlit 
Purpose: In this milestone, you move from concept to construction. You will decide the main pages of your application, sketch each page before coding, specify the visual elements on every page, and then build those pages as a working Streamlit multipage app. Your design decisions must be grounded in the visual design principles (hierarchy, emphasis, contrast, alignment, whitespace, Gestalt, typography, color, scale & proportion, balance, consistency, unity & variety) and core design frameworks (Norman, Shneiderman, Tognazzini, Rams) covered in class. You will also implement data visualizations and conduct a design self-review using the Visual Design Review Checklist. 
Important: Throughout this milestone, reference your Milestone 1 (M1) persona, design principles, usability targets, and heuristic evaluation findings. Your design decisions should be traceable back to M1. If there are changes from M1, you don't need to update your M1 deliverable, but document what changed and why in your Design Justification. 
Deliverables (submit as one PDF + code repository link): 
1. Page Architecture Plan (with sketches): Sketches for all pages (minimum 4) showing layout, key UI elements, and how users move between pages. Include a simple list naming each page and its purpose. 
2. Working Streamlit Multipage Application: Multipage application with functional navigation, input widgets, and display elements. Code must run without errors. 
3. Data Visualizations: At least 2 charts/visualizations integrated into your app. Charts should respond to user input or filters. 
4. Design Justification: document why you made your design decisions and what changed from sketches to implementation. 
5. Visual Design Review: Review your own app against your milestone 1 design principles and usability targets. What's working? What needs improvement? (1 page)
1. Page Architecture Plan (20 pts) 
Before writing any code, sketch all pages/screens of your application. You can use paper, a whiteboard, a tablet, or any simple tool (such as PowerPoint, Google Slides, or draw.io). The goal is rapid iteration, not polished design. Sketching first helps you plan the layout, navigation, and user flow before getting distracted by implementation details. 
● Page List 
Your app must have at least 4 distinct pages. You decide what pages make sense for your interactive experience.. For each page, provide: 
● Purpose (what users accomplish on this page) 
● User goal it supports (connect to your M1 persona) 
● Sketches 
For each page, create a sketch that shows: 
● Layout structure — where elements are positioned on the page and approximate sizing/proportions. 
● Key UI elements — buttons, inputs, sliders, visuals, navigation 
● Navigation — how users move between pages 
Start with sketching multiple versions quickly. Your first idea is rarely your best. 
● Design Annotations 
Annotate each sketch with at least one visual design principle that guided a placement or grouping decision. 
Examples: "Proximity: grouped filter controls together in sidebar so they read as one unit" or "Hierarchy: metric cards are largest at top because they're the first thing the user needs to see." 
Example of Screens/Pages for Common App Types
App Category 
Typical Screens
E-Commerce App 
Home, Product Listing, Product Detail, Cart, Checkout, Order Confirmation, Order History, Profile, Auth, Spending Stats
Analytics Dashboard 
Dashboard Overview, Analytics/Reports, Data Tables, Detail View, Charts, Settings, Admin Panel, Auth
Task / Project Management 
Dashboard, Data Table, Detail View, Calendar, Activity Feed, Progress/Reports, Settings, Auth
Booking / Reservation App 
Home, Search/Results, Detail View, Calendar, 
Checkout/Payment, Trip Stats, Confirmation, Order History, Auth
Content / Media App 
Home/Feed, Explore, Media Player, Content Detail, Profile,





Search, Listening/Viewing Stats,Notifications, Auth
Educational / Learning App 
Home, Course Catalog, Progress Dashboard, Lesson View, Progress Dashboard, Quiz/Assessment, Profile, Auth
Health / Fitness App 
Dashboard, Activity Log, Calendar, Detail View, Settings, Profile, Progress/Trends, Onboarding, Auth



2. Basic Application Implementation (40 pts) 
Build all planned pages as a working Streamlit multipage application. Your implementation should reflect the page architecture, sketches, and visual design specifications from the sections above. 
● Layout & Structure (15 pts) 
● Use at least 2 layout primitives: st.sidebar, st.columns or st.expander ● Organize controls logically (e.g., filters in sidebar, results in main area) ● Include clear page title and section headers 
● Input Widgets (15 pts) 
● Include at least 5 distinct interactive widgets across your pages (e.g., 
st.selectbox, st.slider, st.text_input, st.date_input, st.button, st.multiselect, st.toggle, st.radio). Widgets must meaningfully affect what the user sees , not just exist on the page. 
● Widgets should be functional and affect displayed output 
● Use appropriate widget types for the data being collected 
● Performance and Display Elements (10 pts) 
● Use st.cache_data where appropriate. Briefly note (in code comments or your writeup) where and why you applied caching. 
● Display data using st.dataframe or st.table 
● Include appropriate feedback messages (st.success, st.warning, st.info, st.error) ● Use st.metric for key summary statistics where appropriate 
Code must run without errors. Test your application thoroughly before submission. 3. Data Visualization (15 pts) 
Implement interactive data visualizations that serve your persona’s goals. Visualizations must be integrated into your Streamlit pages, not standalone scripts. 
● Include at least 2 different chart types (e.g., line chart, bar chart, pie chart, scatter plot) 
● Charts should be interactive or respond to user filter selections 
● Visualizations must support your persona's goals
● Use Streamlit's built-in charts or integrate Plotly for advanced features 
Chart Selection Guide 
Chart Type 
Best For
Line Chart 
Trends over time (e.g., spending by month, progress over weeks)
Bar Chart 
Comparing categories (e.g., expenses by category, tasks by status)
Pie/Donut Chart 
Part-to-whole relationships (e.g., budget breakdown)
Scatter Plot 
Relationships between two variables (e.g., time spent vs. score)
Heatmap 
Patterns across two dimensions (e.g., activity by day and hour)



4. Design Justification (10 pts) 
Write a brief document explaining your design decisions: 
● How your sketches evolved from your Milestone 1 (persona, design principles, and heuristic evaluation findings) 
● Why did you choose specific widgets for each page? 
● How does your layout and navigation support the user's primary tasks ? ● Why did you select your chart types and how they help your persona ? ● What changed (if any) from your original sketches during implementation and why? 
● What trade-offs (if any) did you make (e.g., simplicity vs. features, aesthetics vs. functionality)? 
5. Visual Design Review (15 pts) 
Conduct a self-review of your implemented pages using the Visual Design Review Checklist covered in class. This is your quality check: does the built app match your design intent? 
Review your app at four levels: 
● Detail View (3 pts): Check typography (correct fonts, sizes, weights), spacing (consistent padding and margins), colors (match your palette), and icon/element alignment. Report at least 2 specific observations (things done well or issues found and fixed). 
● Page-Level View (4 pts): Check visual hierarchy (does the eye flow to the most important element first?), alignment (do elements snap to a consistent grid/column structure?), whitespace (is there breathing room, or is the page cluttered?), and content fit (no overflow, truncation, or orphaned elements). Report at least 2 specific observations. 
● Function-Level View (4 pts): Check that key states are handled: loading states, error states, and success states. Check form validation and that users always know where they are in the app. Report at least 2 specific observations. 
● App-Level View (4 pts): Check that patterns are consistent across all pages (same button styles, same card formats, same color usage). Check that your navigation is
coherent and the overall information architecture is logical. Report at least 2 specific observations. 
For each level, describe what you found and what you fixed (if any). The purpose is to demonstrate that you can critically evaluate your own work using the principles you’ve learned.
Reference: Visual Design Principles 
Use this reference when making design decisions and writing your justification. You do not need to submit this separately, but your work should demonstrate these concepts. 
Visual Design Principles 
Principle 
Application
Hierarchy 
Size, color, and placement indicate importance
Emphasis 
Draw attention to key elements through contrast
Contrast 
Differentiate elements through color, size, or weight
Alignment 
Create visual connections through consistent positioning
Whitespace 
Give elements room to breathe; reduce cognitive load
Consistency 
Same patterns for same functions throughout
Typography 
Font choices and size hierarchy create structure
Color 
Semantic meaning (success/warning/error) and brand identity



Gestalt Principles 
Principle 
How to Apply
Proximity 
Place related items close together
Similarity 
Use same colors/shapes for similar functions
Common Region 
Use containers or backgrounds to group elements
Continuity 
Align elements to create visual flow
Closure 
Users perceive complete shapes from partial elements
Figure-Ground 
Make important elements stand out from background



Core Design Frameworks
Framework 
Principle
Norman 
Visibility, feedback, constraints, mapping, consistency, affordance
Shneiderman 
Strive for consistency, seek universal usability , offer informative feedback, design dialogs to yield closure, prevent errors and offer recovery, permit easy reversal of actions, keep users in control, reduce short-term memory load
Tognazzini 
Autonomy, discoverability, efficiency, explorable, Fitts's Law, latency, learnability, track state
Rams 
Good design is innovative, useful, aesthetic, understandable, unobtrusive, honest, long-lasting, thorough down to the last detail, environmentally friendly, and involves as little design as possible



