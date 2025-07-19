import gradio as gr
from research_manager_agent import run_research

async def run(company: str, industry: str, query: str):
    async for chunk in run_research(company, industry, query):
        yield chunk


with gr.Blocks(theme=gr.themes.Ocean()) as ui:
    gr.Markdown("Deep Research for Companies")
    gr.Markdown("Generate comprehensive company research reports with AI-powered analysis")
    
    with gr.Row():
        with gr.Column(scale=1):
            org_textbox = gr.Textbox(label="Organization Name",placeholder="e.g. ComplAI",info="The company you want to research")
            industry_textbox = gr.Textbox(label="Industry", placeholder="e.g. Finance, Healthcare, SaaS",info="Primary industry or sector")
            query_textbox = gr.Textbox(label="Research Topic",placeholder="e.g. Analyze competitor pricing strategies",lines=3,info="What specific aspect would you like to research?")
            
            with gr.Row():
                run_button = gr.Button("Start Research", variant="primary", size="lg")
                clear_button = gr.Button("Clear", variant="secondary")
        
        with gr.Column(scale=2):
            report = gr.Markdown(label="Research Report",value="Your research report will appear here...",height=600)
    
    # Event handlers
    run_button.click(fn=run, inputs=[org_textbox, industry_textbox, query_textbox], outputs=report,show_progress=True)
    query_textbox.submit(fn=run, inputs=[org_textbox, industry_textbox, query_textbox], outputs=report,show_progress=True)

    
    clear_button.click(
        lambda: ("", "", "", "Your research report will appear here..."),
        outputs=[org_textbox, industry_textbox, report]
    )

ui.launch(inbrowser=True, share=False)

