Interactive Applications Milestone 1
Thomas Blalock, Jackson Kennedy, Hudson Noyes, Nathan Wan
2/22/2026
1. Product Overview
Part A: Project Concept Statement
Product Name: Sidequest
Target Users: College-age adults who are looking for spontaneous, offline social activities and new friendships.
Core Use: Enable users to instantly discover, host, and join casual, proximity-based social activities in their immediate area.
Problem Solved: There is currently heavy logistical friction and cognitive load required in planning an activity and sending invitations in multiple group chats to friends, especially when someone wants a niche or last-second social activity.
Design Vision: The experience should feel spontaneous, welcoming, and incredibly low-friction. Users should feel confident jumping into new activities through an interface that prioritizes immediate, real-world action over endless scrolling.
Part B: Concept Narrative
Sidequest is an interactive social platform designed for people seeking spontaneous, offline connections, solving the isolation of the modern era by making it effortless to host or join nearby social activities. To facilitate this, the user interface (UI) will be built around a few high-level components: a clean proximity-based discovery feed, a rapid "Host a Quest" creation form, and a live group chat screen for localized coordination. While the UI provides these structural tools, the user experience (UX) focuses on ensuring the journey from opening the app to attending a local activity feels fast, intuitive, and socially encouraging. We will reduce friction by defaulting to the user's immediate location and current time, allowing them to browse and join an activity with a single tap. To build strong user confidence and prevent anxiety-inducing mistakes, the core flow will feature clear, editable previews before posting a new event to the town, alongside easy, guilt-free options to withdraw from a group, ensuring the leap from the digital feed to the physical world is completely seamless.
2. Proto-Persona

"I just want to play a casual game of pickup volleyball tonight without 
having to plan it weeks in advance."
Name: Leo Vance
Age: 24
Role/Context: Graduate Student / Young Professional (Recently moved to Charlottesville)
Tech Comfort Level: High

Background: Leo moved to Charlottesville about a year ago. Between his classes and part-time job, his schedule is highly variable. He has a small circle of friends from his academic program, but he rarely meets people outside that bubble. Because his workload fluctuates, his free time is often spontaneous. He might suddenly realize his Tuesday evening is completely free. When he tries to find something to do, he usually texts his two closest friends; if they are busy, he just ends up staying in his apartment and scrolling Instagram Reels or watching TV.

Goals: 
Meet new people in the community who share his casual interests (like playing board games, hiking, or grabbing a trivia night beer) without having to commit to a formal, recurring club.
Find low-stakes, fun activities nearby on very short notice.
Easily invite others to join an activity he wants to do without worrying about attendance.

Motivations: Leo wants to feel like he actually lives in his city, rather than just existing in his apartment and campus buildings. He wants to escape the habit of endless doom-scrolling when he is bored. For him, success looks like having an unexpected, fun interaction with a few locals on a random weekday night and heading home feeling energized.

Pain points:
Friends Are Usually Busy: It’s hard to plan an event because his friends never have the same schedule.
Existing Platforms Are Too Formal: Events on platforms like Meetup are planned three weeks in advance, and groups are often massive or completely inactive.
High Barrier to Hosting: He just wants three people to play Catan tonight, but setting up a Facebook Group or paying to host a Meetup feels like overkill.
The Intimidation Factor: Showing up alone to a pre-established, tight-knit group of 30 people causes social anxiety. He prefers small, spontaneous, "anyone is welcome" vibes.

Behaviors & habits: 
Checks his phone in short 2-3 minute bursts while walking between classes or waiting for coffee.
Relies heavily on map applications (like Google Maps) to navigate the city.
Defaults to scrolling social media feeds for 1–2 hours on evenings when he doesn't have concrete plans.

Needs / requirements:
Speed & Mobile-First Design: Because he uses his phone in a distracted context, he needs to be able to open the app and see what's happening nearby in less than 3 taps.
Time & Proximity Filtering: The app must default to the here and now. He doesn't need to see an event happening 50 miles away next month; he needs to see what is happening within a 5-mile radius tonight.
Frictionless Coordination: The app must support an immediate group chat or comment thread for an activity so he can easily talk with other people in the event without giving out his phone number.

Scenario / Key Task: It’s 5:30 PM on a Thursday. Leo finishes his assignments early and realizes he has the whole evening free. His usual friends are busy studying. Instead of opening Instagram, he opens Sidequest. The app instantly shows him a feed of activities in his area, ordered by his preferences. He taps one just four blocks away: "Casual Board Games at the Brewery - 6:30 PM." He taps "Join," throws on his shoes, and walks over for a fun night with new friends.
3. Usability Targets
To ensure Sidequest actually feels spontaneous and frictionless, the interface must be highly efficient and forgiving. Below are the specific, measurable targets we will use to evaluate the design's success during testing.
ISO Usability Metrics
Effectiveness: Success means a user can smoothly transition from digital discovery to real-world action. For the primary flow, a successful task is defined as a user locating a nearby activity on the map, tapping "Accept Quest," and successfully viewing the meetup's group chat or exact location details. For the secondary flow, success is defined as a user successfully broadcasting a new activity with a valid title, location, and time.
Efficiency: Because our users (like Leo) will often be checking the app on the go or in distracted environments, speed is critical. "Fast enough" means a user can open the app, find an appealing local event, and join it in under 60 seconds (and in 3 taps or fewer). For hosting, a user should be able to fill out and publish a new Sidequest in under 90 seconds.
Satisfaction: We will gauge satisfaction using a post-task questionnaire (such as the Single Ease Question). After attempting to host or join an event during usability testing, the user must rate the ease of the experience at least a 4 out of 5. Qualitative feedback should heavily feature words like "quick," "easy," or "fun."
Five Components of Usability
Learnability: A first-time user should be able to open the map interface and intuitively understand how to interact with the "pulse" icons to view event details. Without any onboarding tutorials, 80% of new users should successfully complete the task of finding the time and location of an existing event on their very first attempt.
Efficiency: Once the user has learned the basic mechanics, the app should get out of their way. An experienced user should be able to post a new activity (especially a recurring one, like their weekly trivia night) in under 45 seconds by utilizing intuitive forms and smart defaults (like auto-filling their current location).
Memorability: If a user only opens the app intermittently (e.g., once a month when they are exceptionally bored), they should not have to relearn the navigation. A returning user should immediately remember how to toggle between the main Map feed and their active Quests/Messages without tapping the wrong navigation icon first.
Errors: We must prevent anxiety-inducing mistakes, particularly regarding public broadcasts. The error rate for accidentally publishing an incomplete or incorrect event should be less than 5%. If a user does accidentally publish an event prematurely, the system must support immediate recovery: there must be a highly visible, one-tap "Edit" or "Cancel/Delete" button available immediately after posting, ensuring no social penalty for a slip-up.
Satisfaction: The design should feel pleasant, modern, and engaging. Using the kinetic map grid and pulse animations (referenced in our splash page), the interface should invoke a sense of "exploration" rather than "administrative work." During think-aloud testing, we will consider the satisfaction requirement met if users express positive verbal cues (e.g., "Oh, that's cool") when navigating the map or discovering an event.
4. Core Design Principles
For Sidequest to successfully bridge the gap between digital discovery and real-world connection, the interface must actively work to reduce social anxiety and friction. To achieve this, we will rely on the following design principles.

Shneiderman’s "Permit easy reversal of actions"
Where/How: The UI will feature highly visible "Cancel" and "Leave" options on active events, similar to how ride-sharing applications allow a "Cancel" option until the driver's arrival.
Why it matters: Leo feels intimidated by the high stakes of formal event planning. Allowing users to undo their actions freely lets them explore without fear of permanent consequences. This completely removes the pressure from hosting or spontaneously joining a Sidequest.

Rams’ "As little design as possible"
Where/How: The main discovery feed will strip away everything non-essential to concentrate exclusively on what matters. We will prioritize white space and avoid clutter to prevent distraction, heavily mirroring the minimalist approach of Google's homepage.
Why it matters: Because Leo checks his phone in brief, distracted 2-3 minute bursts, he needs an interface that acts as an unobtrusive tool. A minimalist design directly combats his "doom-scrolling" habit by getting straight to the point.

Tognazzini’s "Fitts’s Law"
Where/How: The most critical actions, such as the button to join a meetup, will feature important targets that are large and close. We will place a massive call-to-action button at the bottom of the screen, mimicking the big "Reserve" button pattern used by Airbnb.
Why it matters: Leo often uses the app on the go while walking. Following Fitts's Law ensures he can quickly and accurately accept a quest with a single thumb tap, maximizing his efficiency.

(Visual) Emphasis via Color Contrast
Where/How: We will apply a splash of vivid color against a muted background to instantly pull the user's eye toward immediate, nearby events. This color contrast will effectively create an instant focal point.
Why it matters: Leo's main goal is finding short-notice activities happening right now. By utilizing emphasis, we ensure the viewer's eye goes exactly where the designer intended without any guessing.
5. Heuristic Evaluation of a Similar Interface
Comparable App: Meetup (Mobile Application)

Issue 1
Violated heuristic: #7 Flexibility and efficiency of use
Why it matters: The app keeps pushing its groups concept to the forefront of any exploration of events nearby, Leo’s whole point is to not stick within one group but find things on the fly when needed. This makes his searches need extra taps that increase the amount of interaction needed to do what he views should be a fast and simple task.
Severity rating: 3 (Major)
Suggested fix: Implement a default "Happening Now" feed on home page instead of having to go to explore page and filter things.

Issue 2
Violated heuristic: #8 Aesthetic and minimalist design
Why it matters: Has your profile take up the entire column space at the top instead of just having it in the top left or another corner, makes it so you have to go down farther to get to content. Also there are too many different buttons for type of activity, although they manage by making it scroll horizontally, this should definitely be condensed because Leo wants to access his interests quickly without having to concentrate on finding things.
Severity rating: 3 (Major)
Suggested fix: Condense things like dancing/music/hiking to existing health category and other similar changes.

Issue 3
Violated heuristic: #10 Help and Documentation
Why it matters: You have a question you should be able to get an answer, you shouldn’t have to try to find it. Meetups has no settings or immediately available help section, you have to go to your profile, then go to settings, then scroll to find support.
Severity rating: 2 (Minor)
Suggested fix: Easy access support button.
6. Usability Test Plan
To ensure Sidequest actually delivers on its promise of low-friction, spontaneous social connection, we need to observe how real users interact with the interface before writing the final code.
Part A: Task-Based Usability Testing (Think-Aloud)
We will conduct moderated think-aloud sessions where participants are given scenarios that match Leo's real-world situations.

Task 1: Discovering and Joining an Activity
Scenario: You just finished studying, you have a free evening, and you don't want to sit at home. Find a casual activity happening nearby right now that sounds fun, and let the group know you are coming.
Metrics:
Success/Fail: Success is achieved when the user successfully scrolls the feed, selects an appealing activity, and taps the "Join" (or equivalent) button to join.
Time: Target is under 60 seconds from opening the app to joining.
Errors: Tracking if the user tries to swipe horizontally (like a dating app) instead of scrolling vertically, or if they tap the wrong interactive elements on the feed cards.
Confusion: Noting any hesitation when deciphering how far away an event is, or pauses indicating they don't know how to finalize joining the activity.

Task 2: Hosting a Spontaneous Activity
Scenario: You and two friends are heading to a local brewery for trivia in an hour, but you have room for a couple more people on your team. Broadcast this to the area so a few locals can join you.
Metrics:
Success/Fail: Success is achieved when the user navigates to the creation screen, fills out the title, location, and start time, and successfully publishes it to the local feed.
Time: Target is under 90 seconds.
Errors: Leaving required fields (like location) blank, or accidentally publishing the event before they finish typing the description.
Confusion: Long stops or rereading to figure out what details are mandatory versus optional, or expressing anxiety about who will be able to see the post.

Task 3: Bailing on a Commitment
Scenario: You previously joined a group planning to play volleyball at the park, but it just started raining. You need to back out of the activity so the group isn't waiting for you.
Metrics:
Success/Fail: Success is achieved when the user navigates to their active schedule/itinerary and successfully withdraws from the event.
Time: Target is under 30 seconds.
Errors: Navigating to the general discovery feed to look for the event instead of checking their personal active list.
Confusion: Searching for the cancel option in the wrong place, or pausing out of fear that "canceling" will send a disruptive notification to the whole group.
Part B: A/B Test Plan
Design Decision: Information density on the main discovery feed cards. Because the feed is designed to be scrolled like Instagram rather than searched like a map, I am unsure how much information should be exposed immediately versus hidden behind a tap.
Version A (High Density): Each feed card displays the activity title, host avatar, exact street address, and the first three lines of the description directly in the feed.
Version B (Low Density / Progressive Disclosure): Each feed card displays only the activity title, a visual thumbnail, the start time, and the relative distance (e.g., "0.5 miles away"). The user must tap the card to reveal the exact address and full description.
Hypothesis: I predict Version B will perform better. By keeping the interface unobtrusive and reducing the short-term memory load, users will be able to scan the feed much faster. High density might cause cognitive overload, making the app feel too much like a reading assignment.
Metric to Decide the Winner: Time on task (how quickly they can scan and select an event they like) and the subjective ease-of-use rating (1-5 scale) asked immediately after the task.
Success Criteria: Version B wins if it reduces the average time to select an event by ≥ 15% without negatively impacting the subjective ease-of-use rating. If the difference is negligible, we will default to Version A to save users the extra tap.

