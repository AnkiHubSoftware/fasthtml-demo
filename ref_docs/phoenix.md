


datasets


GET
/v1/datasets
List datasets



DELETE
/v1/datasets/{id}
Delete dataset by ID



GET
/v1/datasets/{id}
Get dataset by ID



GET
/v1/datasets/{id}/versions
List dataset versions



POST
/v1/datasets/upload
Upload dataset from JSON, CSV, or PyArrow



GET
/v1/datasets/{id}/examples
Get examples from a dataset



GET
/v1/datasets/{id}/csv
Download dataset examples as CSV file



GET
/v1/datasets/{id}/jsonl/openai_ft
Download dataset examples as OpenAI fine-tuning JSONL file



GET
/v1/datasets/{id}/jsonl/openai_evals
Download dataset examples as OpenAI evals JSONL file


experiments


POST
/v1/datasets/{dataset_id}/experiments
Create experiment on a dataset



GET
/v1/datasets/{dataset_id}/experiments
List experiments by dataset



GET
/v1/experiments/{experiment_id}
Get experiment by ID



GET
/v1/experiments/{experiment_id}/json
Download experiment runs as a JSON file



GET
/v1/experiments/{experiment_id}/csv
Download experiment runs as a CSV file


spans


POST
/v1/span_annotations
Create or update span annotations


traces


POST
/v1/evaluations
Add span, trace, or document evaluations



GET
/v1/evaluations
Get span, trace, or document evaluations from a project


prompts


GET
/v1/prompts
Get all prompts



POST
/v1/prompts
Create a prompt version



GET
/v1/prompts/{prompt_identifier}/versions
List all prompt versions for a given prompt



GET
/v1/prompt_versions/{prompt_version_id}
Get prompt by prompt version ID



GET
/v1/prompts/{prompt_identifier}/tags/{tag_name}
Get prompt by tag name



GET
/v1/prompts/{prompt_identifier}/latest
Get the latest prompt version


default


GET
/exports
Download Exported File