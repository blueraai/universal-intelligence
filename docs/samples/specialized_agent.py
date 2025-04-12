"""
Specialized Domain Agent Example

This example demonstrates how to create a domain-specific agent:
- Configuring a model with domain-specific settings
- Creating domain-specific tools
- Creating a specialized agent
- Processing domain-specific requests
"""

from universal_intelligence import Model, Tool, Agent

# Initialize with a domain-specific model configuration
# The configuration adjusts the model for financial domain tasks
financial_model = Model(
    configuration={
        "processor": {
            "input": {
                "tokenizer": {
                    "trust_remote_code": True
                },
                "chat_template": {
                    "add_generation_prompt": True
                }
            },
            "output": {
                "skip_special_tokens": True,
                "clean_up_tokenization_spaces": True
            }
        },
        "model": {
            "device_map": "auto",
            "torch_dtype": "auto"
        }
    }
)

print("=== Financial Domain Agent ===")
print("Initialized model with financial domain configuration")

# Create domain-specific tools
# In a real application, this would connect to financial data sources
market_data_tool = Tool(configuration={
    "api_key": "sample_key",
    "base_url": "https://api.marketdata.example.com"
})

stock_analysis_tool = Tool(configuration={
    "api_key": "sample_key",
    "base_url": "https://api.stockanalysis.example.com"
})

print("\n=== Domain-Specific Tools ===")
print("Market Data Tool: Provides real-time and historical market data")
print("Stock Analysis Tool: Provides fundamental and technical analysis")

# Create specialized agent for financial advising
financial_advisor_agent = Agent(
    universal_model=financial_model,
    expand_tools=[market_data_tool, stock_analysis_tool]
)

print("\n=== Financial Advisor Agent ===")
print("Specialized agent created with financial model and domain-specific tools")

# Process domain-specific request
query = "What's the outlook for technology stocks this quarter?"
print(f"\n=== Processing Domain Query ===")
print(f"Query: {query}")

result, logs = financial_advisor_agent.process(query)

print("\n=== Financial Advisor Response ===")
print(result)

print("\n=== Domain Specialization Benefits ===")
print("1. Enhanced domain knowledge through specialized model configuration")
print("2. Access to domain-specific data via specialized tools")
print("3. Better performance on domain-specific tasks")
print("4. More accurate and relevant responses for the domain")

# Example of providing domain-specific context
print("\n=== Domain-Specific Context Example ===")

# Sample financial context data
financial_context = [
    "The Federal Reserve announced a 25 basis point rate cut yesterday.",
    "Technology sector earnings have exceeded expectations by 15% this quarter.",
    "Cloud computing companies have seen a 30% increase in enterprise adoption."
]

print("Adding domain-specific context to the query")
result, logs = financial_advisor_agent.process(
    "How might these conditions affect investment strategies for tech stocks?",
    context=financial_context
)

print("\n=== Contextualized Domain Response ===")
print(result)

"""
Sample output:

=== Financial Advisor Response ===
Based on current market indicators and analyst projections, the outlook for technology stocks this quarter appears cautiously optimistic. Several factors support this assessment:

1. Earnings Growth: Many major technology companies have reported stronger-than-expected earnings in recent reports.

2. AI Investment: Continued investment in artificial intelligence is driving growth particularly in semiconductor, cloud computing, and software sectors.

3. Adoption Trends: Enterprise digital transformation initiatives remain robust, supporting demand for cloud services, cybersecurity, and enterprise software.

However, there are some moderating factors to consider:

1. Valuation Concerns: Many technology stocks are trading at elevated multiples, which may limit upside potential.

2. Regulatory Scrutiny: Ongoing antitrust and regulatory concerns could impact larger technology firms.

3. Interest Rate Sensitivity: Technology growth stocks can be sensitive to interest rate expectations.

For investors considering technology stocks this quarter, a selective approach focusing on companies with strong fundamentals, reasonable valuations, and exposure to durable growth trends would be prudent.
"""
