## Analysis Report: Socioeconomic Factors and Healthcare Burden during COVID-19 in the Americas

## 1 Introduction

The COVID-19 pandemic showed big differences in healthcare systems and how countries handled challenges across the Americas. This region, with countries at different economic levels, faced many problems with the healthcare burden. Poorer countries struggled with more infections and deaths, while richer countries had better responses, though not always successful.
Simple factors like income, healthcare systems, and population size affected how countries dealt with the pandemic. Nations with less money and more people had bigger problems, like hospitals running out of space and slow vaccine delivery, which showed their weaknesses.
This report looks at how socioeconomic factors affected healthcare during the COVID-19 pandemic in the Americas. It focuses on one question:  
**“How do socioeconomic factors influence the healthcare burden caused by COVID-19 in the Americas?”**

## 2 Used Data

This analysis uses two datasets: **"Our World in Data COVID-19 Dataset"** and **"World Bank Open Data."** Both datasets were processed to get the needed information for studying how socioeconomic factors affected healthcare during COVID-19 in the Americas.

### 1. Our World in Data COVID-19 Dataset

- **Source**: This dataset comes from Our World in Data. It contains time-series data about the COVID-19 pandemic.
- **Structure and Characteristics**: The dataset includes information for more than 200 countries. It has data like confirmed cases, deaths, testing rates, ICU patients, and vaccinations. After processing, the dataset was filtered to include only countries in the Americas. Key indicators, like deaths per 100,000 people and vaccination rates, were used.
- **License Compliance**: The dataset follows the CC BY 4.0 License. It allows sharing and changes if proper credit is given. Credit to Our World in Data has been included in this work.

### 2. World Bank Open Data

- **Source**: This dataset is from the World Bank. It has socioeconomic indicators for over 200 countries.
- **Structure and Characteristics**: The dataset includes data like GDP, unemployment, Gini index, poverty, healthcare spending, and urbanization. Data for countries in the Americas was taken and matched with the COVID-19 dataset to show links between socioeconomic factors and healthcare outcomes.
- **License Compliance**: This dataset follows the World Bank Terms of Use. It allows non-commercial use with proper credit. Credit to the World Bank is included in this work.

## 3 Analysis

This section presents the methods, results, and interpretations of the analysis conducted to understand how socioeconomic factors influenced the healthcare burden caused by COVID-19 in the Americas. The analysis involved correlation studies and exploratory visualizations to highlight relationships and trends.

### 3.1 Correlation Analysis

To identify relationships between COVID-19 metrics and socioeconomic indicators, a correlation matrix was created. Several key findings were observed:

- **COVID-19 deaths per capita** were strongly correlated with **GDP per capita**, suggesting that wealthier nations experienced higher confirmed death rates, potentially due to better testing and reporting mechanisms.
- **Vaccination rates** showed a positive correlation with **healthcare expenditure**, highlighting the role of investment in healthcare systems.
- **Poverty** and **Gini index** (income inequality) had weaker correlations with COVID-19 metrics, but they still influenced healthcare outcomes indirectly.

<div style="display: flex; align-items: center; justify-content: flex-start;">
  <div style="flex: 1; margin-right: 20px;">
    <p><strong>Key Insights:</strong></p>
    <ul>
      <li>Strong correlations between deaths and GDP per capita.</li>
      <li>Vaccination correlated positively with healthcare spending.</li>
      <li>Weaker correlations with poverty and inequality.</li>
    </ul>
  </div>
  <div style="flex: 1; text-align: center;">
    <img src="/Users/wangyulin/MADE/made-yulinwang/data/correlation.png" alt="Correlation Matrix" style="width: 70%; margin: auto;">
    <p style="font-size: 12px; text-align: center;">Figure 1. Correlation Matrix of COVID-19 Metrics and Socioeconomic Indicators</p>
  </div>
</div>

### 3.2 Exploratory Analysis

#### 3.2.1 Healthcare System and Outcomes Over Time

Time-series plots were generated to visualize healthcare-related metrics, including hospital beds per thousand, ICU patients per million, total cases, and total deaths across countries in the Americas. Several insights were identified:

- **Hospital bed availability** remained relatively constant over time, suggesting limited investments in expanding capacity during the pandemic.
- **ICU usage** peaked in 2021, reflecting the strain on healthcare systems during severe waves of the pandemic.
- **Total cases and deaths** showed consistent growth, with significant differences among countries, likely due to variations in population size, healthcare systems, and government responses.

<p style="text-align: center;">
  <img src="/Users/wangyulin/MADE/made-yulinwang/data/analysis1.png" alt="Healthcare System and Outcomes" style="width: 50%;">
</p>
<p style="font-size: 12px; text-align: center;">Figure 2. Healthcare System and Outcomes Over Time</p>

#### 3.2.2 Economic and Social Factors Over Time

Economic and social indicators, such as GDP per capita, life expectancy, poverty rates, and healthcare expenditure, were analyzed to understand their evolution during the pandemic. Key observations include:

- **GDP per capita** saw a sharp decline in 2020, reflecting the economic impact of COVID-19, followed by slow recovery in subsequent years.
- **Poverty rates** increased in lower-income nations, highlighting the socioeconomic burden of the pandemic.
- **Healthcare expenditure** increased in many countries during the pandemic, reflecting efforts to combat the crisis.

<p style="text-align: center;">
  <img src="/Users/wangyulin/MADE/made-yulinwang/data/analysis2.png" alt="Economic and Social Factors" style="width: 50%;">
</p>
<p style="font-size: 12px; text-align: center;">Figure 3. Economic and Social Factors Over Time</p>

#### 3.2.3 Vaccination and Urbanization Trends

Vaccination rates and urbanization levels were analyzed to explore their impacts on pandemic outcomes. Key insights include:

- **Vaccination rates** varied significantly among countries, with wealthier nations achieving higher coverage earlier.
- **Urbanization rates** were relatively stable, but countries with higher urbanization faced challenges in controlling the spread due to population density.

<p style="text-align: center;">
  <img src="/Users/wangyulin/MADE/made-yulinwang/data/analysis3.png" alt="Vaccination and Urbanization Trends" style="width: 50%;">
</p>
<p style="font-size: 12px; text-align: center;">Figure 4. Vaccination and Urbanization Trends</p>

## 4 Conclusions

This study aimed to explore how socioeconomic factors influenced the healthcare burden caused by COVID-19 in the Americas. The findings reveal significant relationships between socioeconomic indicators and key healthcare outcomes, highlighting disparities in the region's ability to manage the pandemic.

### Key Findings
- **Correlation Insights**: 
   - Higher GDP per capita was associated with increased deaths per capita, potentially due to more comprehensive reporting and testing mechanisms in wealthier nations.
   - Investment in healthcare infrastructure, such as ICU capacity and vaccination programs, played a crucial role in mitigating healthcare strain.

### Reflection
The study successfully addressed the primary research question by uncovering clear connections between socioeconomic factors and the healthcare burden during COVID-19. However, some limitations remain:
- **Data Completeness**: Gaps in ICU capacity and vaccination rate data for certain countries may have affected the reliability of the analysis.
- **Time Constraints**: The datasets only covered a limited time range, making it challenging to capture long-term trends or fully assess the pandemic's aftermath.

### Future Research Directions
Further research could explore:
- The long-term relationship between socioeconomic factors and healthcare outcomes across multiple pandemics.
- Improved data collection methods to minimize biases and better represent vulnerable regions.

By addressing these limitations, future studies could provide deeper insights into how to enhance global resilience to health crises.
