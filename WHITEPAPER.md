# CigarMatch - Design Decisions & Rationale

## Problem Statement
Cigar enthusiasts lack a **personalized subscription service** that curates cigars based on their taste preferences. Existing services offer generic selections, leaving users to manually research and purchase cigars that match their preferences.

## Design Decisions

### 1. Backend: Flask
- **Why Flask?** Lightweight, easy to set up, and ideal for small-scale web apps. Flask's simplicity accelerates MVP development.
- **Why SQLite?** File-based, no server required, and perfect for prototyping. Scales to thousands of users before needing a dedicated database.

### 2. Frontend: HTML/CSS/JS + Bootstrap 5
- **Why Bootstrap?** Ensures a responsive, mobile-friendly UI with minimal effort. Reduces frontend development time.
- **Why Vanilla JS?** Simplifies deployment and avoids heavy frameworks like React. Keeps the codebase lightweight and easy to maintain.

### 3. AI Engine: Rule-Based MVP
- **Description**: The MVP uses a **rule-based recommendation engine** to suggest cigars based on user preferences (strength, wrapper, origin, price). This avoids the complexity of ML while delivering personalized results.
- **Trade-offs**: Rule-based systems are less accurate than ML but are **faster to develop** and **easier to debug**. Future work will transition to ML (e.g., collaborative filtering).

### 4. Database Schema
- **Users**: Stores user credentials and roles (user/admin).
- **Cigars**: Inventory of cigars with attributes (name, brand, strength, wrapper, origin, price range, description).
- **UserPreferences**: Stores user preferences for recommendations.
- **Subscriptions**: Tracks active subscriptions and their details.

## Challenges & Solutions

### 1. Reddit API Restrictions
- **Challenge**: Reddit's API and web frontend blocked automated access (403 Forbidden).
- **Solution**: Synthesized the project idea from search results and [SomebodyMakeThis.org](https://somebodymakethis.org/).

### 2. Mock AI for Prototyping
- **Challenge**: Full AI model integration (e.g., ML-based recommendations) is complex and resource-intensive.
- **Solution**: Used a **rule-based mock AI** for rapid prototyping. This ensures the app works without relying on external services or heavy ML models.

### 3. Offline Support
- **Challenge**: Users may not have access to external APIs or databases.
- **Solution**: SQLite and mock data ensure the app works **offline** and without external dependencies.

## Future Work
- **User Authentication**: Add login via Google/GitHub for a seamless onboarding experience.
- **ML Recommendations**: Transition from rule-based to ML-based recommendations (e.g., collaborative filtering).
- **Payment Integration**: Add Stripe/PayPal for subscription payments.
- **User Reviews**: Allow users to rate and review cigars to improve recommendations.
- **Mobile App**: Develop a mobile app for iOS/Android using React Native.

## License
MIT