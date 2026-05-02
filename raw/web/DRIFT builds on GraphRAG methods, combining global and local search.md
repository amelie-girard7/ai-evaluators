---
title: DRIFT builds on GraphRAG methods, combining global and local search
source: https://www.microsoft.com/en-us/research/blog/introducing-drift-search-combining-global-and-local-search-methods-to-improve-quality-and-efficiency/
author:
- '[[Brenda Potts]]'
published: 2024-11-01
created: 2026-05-01
description: 'GraphRAG leverages semantic structuring of data to generate responses
  to complex user queries. A collaboration with Uncharted expands the frontiers of
  this technology, developing a new approach to processing local queries: DRIFT search:'
tags:
- clippings
processed: true
processed_at: '2026-05-01'
---
![Three icons that represent local and global search and GraphRAG. These icons sit on a blue to pink gradient.](https://www.microsoft.com/en-us/research/wp-content/uploads/2024/10/DRIFT-Search-GraphRAG-BlogHeroFeature-1400x788-1.jpg)

Three icons that represent local and global search and GraphRAG. These icons sit on a blue to pink gradient.

GraphRAG is a technique that uses large language models (LLMs) to create knowledge graphs and summaries from unstructured text documents and leverages them to improve retrieval-augmented generation (RAG) operations on private datasets. It offers comprehensive global overviews of large, private troves of unstructured text documents while also enabling exploration of detailed, localized information. By using LLMs to create comprehensive knowledge graphs that connect and describe entities and relationships contained in those documents, GraphRAG leverages semantic structuring of the data to generate responses to a wide variety of complex user queries. [Uncharted](http://uncharted.software/), one of Microsoft’s research collaborators, has recently been expanding the frontiers of this technology by developing a new approach to processing local queries: DRIFT search (Dynamic Reasoning and Inference with Flexible Traversal). This approach builds upon Microsoft’s GraphRAG technique, combining characteristics of both global and local search to generate detailed responses in a method that balances computational costs with quality outcomes.

## How GraphRAG works

GraphRAG has two primary components, an indexing engine and a query engine.

The indexing engine breaks down documents into smaller chunks, converting them into a knowledge graph with entities and relationships. It then identifies communities within the graph and generates summaries—or “community reports”—that represent the global data structure.

The query engine utilizes LLMs to build graph indexes over unstructured text and query them in two primary modes:

- **Global search** handles queries that span the entire dataset. This mode synthesizes information from diverse underlying sources to answer questions that require a broad understanding of the whole corpus. For example, in a dataset about tech company research efforts, a global query could be: “What trends in AI research have emerged over the past five years across multiple organizations?” While effective for connecting scattered information, global search can be resource intensive.
- **Local search** optimizes for targeted queries, drawing from a smaller subset of documents that closely match the user’s input. This mode works best when the answer lies within a small number of text units. E.g. a query asking: “What new features and integrations did Microsoft’s Cosmos DB team release on October 4th?”

The creation of these summaries often involves a human in the loop (HITL), as user input shapes how information is summarized (e.g., what kinds of entities and relationships are extracted). To index documents using GraphRAG, a clear description of the intended user persona (as defined in the indexing phase) is needed, as it influences how nodes, edges, and community reports are structured.

## Introducing DRIFT Search

DRIFT Search introduces a new approach to local search queries by including community information in the search process. This greatly expands the breadth of the query’s starting point and leads to retrieval and usage of a far higher variety of facts in the final answer. This addition expands the GraphRAG query engine by providing a more comprehensive option for local search, which uses community insights to refine a query into detailed follow-up questions. These follow-ups allow DRIFT to handle queries that may not fully align with the original [extraction templates](https://www.microsoft.com/en-us/research/blog/graphrag-auto-tuning-provides-rapid-adaptation-to-new-domains/) defined by the user at index time.

| Answer details | Drift (DS\_Default) | Local (LS) |
| --- | --- | --- |
| Supply Chain | Traced back to cinnamon in Ecuador and Sri Lanka   \[Redacted Brand\] and \[Redacted Brand\] Brands Impacted   Products sold at \[Redacted Brand\] and \[Redacted Brand\] | Plants in Ecuador |
| Contamination Levels | 2000 times higher than FDA max | Blood lead levels ranging from 4 to 29 micrograms per deciliter |
| Actions | Recalls and health advisories   Investigating plant in Ecuador   Issued warnings to retailers | Recalls and health advisories |

**Table 1**: An example of summarized responses from two search techniques (DRIFT and Local Search) on a dataset of AP News articles to the query**: “** Describe what actions are being taken by the U.S. Food and Drug Administration and the Centers for Disease Control and Prevention to address the lead contamination in apple cinnamon fruit puree and applesauce pouches in the United States during November 2023”. As shown in the table, DRIFT search was able to surface details not immediately available with the two other approaches.

## DRIFT Search: A step-by-step process

1. **Primer:** When a user submits a query, DRIFT compares it to the top K most semantically relevant community reports. This generates an initial answer along with several follow-up questions, which act as a lighter version of global search. To do this, we expand the query using Hypothetical Document Embeddings (HyDE), to increase sensitivity (recall), embed the query, look up the query against all community reports, select the top K and then use the top K to try to answer the query. The aim is to leverage high-level abstractions to guide further exploration.
2. **Follow-Up:** With the primer in place, DRIFT executes each follow-up using a local search variant. This yields additional intermediate answers and follow-up questions, creating a loop of refinement that continues until the search engine meets its termination criteria, which is currently configured for two iterations (further research will investigate reward functions to guide terminations). This phase represents a globally informed query refinement. Using global data structures, DRIFT navigates toward specific, relevant information within the knowledge graph even when the initial query diverges from the indexing persona. This follow-up process enables DRIFT to adjust its approach based on emerging information.
3. **Output Hierarchy:** The final output is a hierarchy of questions and answers ranked on their relevance to the original query. This hierarchical structure can be customized to fit specific user needs. During benchmark testing, a naive map-reduce approach aggregated all intermediate answers, with each answer weighted equally.
![An image that shows a hierarchical tree with each node represented as a pie chart of weighting. ](https://www.microsoft.com/en-us/research/wp-content/uploads/2024/10/414141-original-w-labels.png)

Figure 1. An entire DRIFT search hierarchy highlighting the three core phases of the DRIFT search process. A (Primer): DRIFT compares the user’s query with the top K most semantically relevant community reports, generating a broad initial answer and follow-up questions to steer further exploration. B (Follow-Up): DRIFT uses local search to refine queries, producing additional intermediate answers and follow-up questions that enhance specificity, guiding the engine towards context-rich information. A glyph on each node in the diagram shows the confidence the algorithm has to continue the query expansion step. C (Output Hierarchy): The final output is a hierarchical structure of questions and answers ranked by relevance, reflecting a balanced mix of global insights and local refinements, making the results adaptable and comprehensive.

### Why DRIFT search is effective

DRIFT search excels by dynamically combining global insights with local refinement, enabling navigation from high-level summaries down to original text chunks within the knowledge graph. This layered approach ensures that detailed, context-rich information is preserved even when the initial query diverges from the persona used during indexing. By decomposing broad questions into fine-grained follow-ups, DRIFT captures granular details and adjusts based on the emerging context, making it adaptable to diverse query types. This makes it particularly effective when handling queries that require both breadth and depth without losing specific details.

### Benchmarking DRIFT search

As shown, we tested the effectiveness of DRIFT search by performing a comparative analysis across a variety of use cases against GraphRAG local search and a highly tuned variant of semantic search methods. The analysis evaluated each method’s performance based on key metrics such as:

- **Comprehensiveness**: Does the response answer all aspects of the question?
- **Diversity of responses**: Does the response provide different perspectives and insights on the question?

In our results, DRIFT search provided significantly better results on both comprehensiveness and diversity in the metrics. We set up an experiment where we ingested 5K+ news articles from the Associated Press and ingested those articles using GraphRAG. After ingestion, we generated 50 “local” questions on this dataset and used both DRIFT and Local Search to generate answers for each of these questions. These “local” questions were questions that target specific details in the dataset that could be attributed to a small number of text units containing the answer. These answers were then used with an LLM judge to score for comprehensiveness and diversity.

- On comprehensiveness, DRIFT search outperformed Local Search 78% of the time.
- On diversity, DRIFT search outperformed Local Search 81% of the time.

## Availability

DRIFT search is available now on the [GraphRAG GitHub](https://github.com/microsoft/graphrag).

## Future research directions

A future version of DRIFT will incorporate an improved version of Global Search that will allow it to more directly address questions currently serviced best by global search. The hope is to then move towards a single query interface that can service questions of both local and global varieties. This work will further evolve DRIFT’s termination logic, potentially through a reward model that balances novel information with redundancy. Additionally, executing follow-up queries using either global or local search modes could improve efficiency. Some queries require broader data access, which can be achieved by leveraging a query router and a lite- **global search** variant that uses fewer community reports, tokens, and overall resources.

DRIFT search is the first of several major optimizations to GraphRAG that are being explored. It shows how a global index can even benefit local queries. In our future work, we plan to explore more approaches to bring greater efficiency to the system by leveraging the knowledge graph that GraphRAG creates.