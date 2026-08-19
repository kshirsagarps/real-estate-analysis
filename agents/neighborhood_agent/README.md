# Neighborhood Agent (`neighborhood_agent`)

The **Neighborhood Agent** provides hyper-local location intelligence, assessing quality of life, family desirability, and growth trajectories.

## Responsibilities & Scope
1. **School District Analysis**: Retrieves GreatSchools ratings (Elementary, Middle, High School).
2. **Safety & Crime Data**: Evaluates local safety indexes and violent/property crime rates vs national averages.
3. **Walkability & Infrastructure**: Assesses Walk Score, Transit Score, bikeability, and proximity to grocery stores/employment hubs.
4. **Demographic & Economic Growth**: Evaluates population growth, median household income trends, and job growth.
5. **Outputs**:
   - School rating composite ($1\text{--}10$).
   - Safety score and crime rating.
   - Neighborhood grade & trajectory (Improving, Stable, Declining).
   - Category Score for **Neighborhood Quality (0-100)**.

## Model & Performance
- **Model**: `Gemini Flash` (rapid web retrieval & demographic data extraction).
- **Execution Mode**: Concurrent parallel execution.
