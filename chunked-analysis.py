from anthropic import Anthropic
import json
import logging
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

model="claude-3-5-sonnet-20241022"

def chunk_statements(statements, chunk_size=40):
    """Split statements into manageable chunks"""
    return [statements[i:i + chunk_size] for i in range(0, len(statements), chunk_size)]

def analyze_chunk(client, statements, chunk_num, total_chunks):
    """Analyze a single chunk of statements"""
    chunk_data = json.dumps(statements)
    
    prompt = f"""You are an expert political analyst with deep expertise in UK politics and electoral messaging, specifically supporting the Labour Party's research division. Your task is to conduct a detailed analysis of Reform UK candidate statements from chunk {chunk_num} of {total_chunks}.
        Analysis Framework
        Analyse the statements according to these key dimensions:
        1. Thematic Analysis

        Identify primary campaign themes and messaging priorities
        Note recurring ideological positions and worldviews
        Track references to specific political events or issues
        Analyse how themes align with or contrast against mainstream conservative positions

        2. Policy Position Analysis

        Document specific policy proposals and positions
        Categorize policies by domain (economic, social, immigration, etc.)
        Identify the level of detail and specificity in policy proposals
        Note any costing or implementation details provided
        Track alignment with or divergence from Reform UK's national platform

        3. Rhetorical Analysis

        Identify recurring linguistic patterns and persuasive techniques
        Document emotional appeals and trigger words
        Analyse framing of issues and opponents
        Note metaphors and analogies used
        Track populist vs establishment messaging patterns

        4. Evidence Collection

        Extract verbatim quotes that best exemplify key positions
        Document specific claims and statistical assertions
        Note references to external sources or authorities
        Track mentions of specific locations, demographics, or constituencies

        5. Comparative Elements

        Note any distinct regional messaging patterns
        Identify variations in candidate messaging styles
        Track alignment with national Reform UK messaging
        Document any notable departures from party line

        Input Format:
        The statements are provided in JSON format:
        {chunk_data}
        Output Structure:
        Present your analysis in clear sections corresponding to the framework above, with specific examples and quotes where relevant. Remember this is chunk {chunk_num} of {total_chunks}, so focus on patterns within this specific set while noting potential connections to broader trends.
        Additional Considerations:
        Maintain objective analytical tone while focusing on strategic value
        Support all conclusions with specific examples
        Note degrees of confidence in pattern identification
        Flag potential sampling biases or limitations
        Include quantitative measures where possible (e.g., frequency of theme occurrence)
        Consider implications for Labour's electoral strategy        
        """
    response = client.messages.create(
        model=model,
        max_tokens=8192,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def synthesize_results(client, analyses):
    """Create final synthesis of all chunk analyses"""
    synthesis_prompt = f"""You are a senior political analyst specializing in opposition research and electoral strategy for the Labour Party. Your task is to synthesize analyses from {len(analyses)} distinct sets of Reform UK candidate statements into a comprehensive strategic intelligence report.
Synthesis Framework
1. Strategic Theme Analysis

Identify and rank the most significant recurring themes across all chunks
Map the evolution or variation of themes across different chunks
Analyze the relationship between local and national messaging
Evaluate the effectiveness and potential vulnerabilities in messaging

2. Policy Platform Assessment

Synthesize key policy positions that appear consistently
Identify areas of policy consensus and divergence
Analyze the depth and practicality of policy proposals
Map potential contradictions or inconsistencies
Evaluate alignment with voter concerns and Labour positions

3. Rhetorical Strategy Mapping

Document dominant persuasive techniques and their frequency
Analyze the effectiveness of language patterns
Identify target audiences based on rhetorical choices
Map emotional triggers and appeal patterns
Analyze framing of key issues and opponents

4. Regional and Demographic Analysis

Map geographical variations in messaging
Identify constituency-specific adaptations
Track demographic targeting patterns
Note effectiveness of localization strategies

5. Strategic Implications

Identify key vulnerabilities in Reform UK messaging
Map potential counter-messaging strategies
Document opportunities for Labour positioning
Analyze potential impact on Conservative vote share

Input Format:
Previous analyses provided as:
{'\n\n'.join(f'Chunk {i+1} Analysis:\n{analysis}' for i, analysis in enumerate(analyses))}
Output Structure:
Present a comprehensive analysis that synthesizes all chunks into a coherent strategic intelligence report, organized according to the framework above. Include specific examples and quotes where they illustrate significant patterns or conclusions.

Additional Considerations:
Maintain objective analytical tone while focusing on strategic value
Support all conclusions with specific examples
Note degrees of confidence in pattern identification
Flag potential sampling biases or limitations
Include quantitative measures where possible (e.g., frequency of theme occurrence)
Consider implications for Labour's electoral strategy
"""
    response = client.messages.create(
        model=model,
        max_tokens=8192,
        temperature=0,
        messages=[{"role": "user", "content": synthesis_prompt}]
    )
    return response.content[0].text

def main():
    logging.info("Loading data")
    with open('statements.json', 'r') as file:
        data = json.load(file)
    logging.info("Data loaded")

    # Initialize Anthropic client
    anthropic_client = Anthropic()
    
    # Split into chunks
    chunks = chunk_statements(data)
    logging.info(f"Processing {len(chunks)} chunks of statements...")
    
    # Analyze each chunk
    chunk_analyses = []
    for i, chunk in enumerate(chunks, 1):
        logging.info(f"Processing chunk {i}/{len(chunks)}...")
        try:
            analysis = analyze_chunk(anthropic_client, chunk, i, len(chunks))
            chunk_analyses.append(analysis)
            
            # Save intermediate results
            with open(f'chunk_analysis_{i}.txt', 'w') as f:
                f.write(analysis)
                
            sleep(2)  # Rate limiting
        except Exception as e:
            logging.error(f"Error processing chunk {i}: {e}")
    # for i in range(1, 14):
    #     with open(f'chunk_analysis_{i}.txt', 'r') as f:
    #         chunk_analyses.append(f.read())
    
    # Generate final synthesis
    logging.info("Generating final synthesis...")
    try:
        final_analysis = synthesize_results(anthropic_client, chunk_analyses)
        
        # Save final analysis
        with open(f"{model}.txt", 'w') as file:
            file.write(final_analysis)
        logging.info("Analysis complete! Results saved")
    except Exception as e:
        logging.error(f"Error in final synthesis: {e}")

if __name__ == "__main__":
    main()
