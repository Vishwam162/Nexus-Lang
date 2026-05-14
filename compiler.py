import os, sys, threading, time, webbrowser
from google import genai 
from flask import Flask

class NexusInterpreter:
    def __init__(self):
        self.vars = {}
        self.agent_persona = "Assistant"
        self.agent_task = "Analyze"
        self.html_buffer = ""
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else None

    def walk(self, node):
        if not isinstance(node, tuple): return node
        tag = node[0]
        if tag == 'num' or tag == 'str': return node[1]
        if tag == 'var': return self.vars.get(node[1], 0)
        if tag == 'let': self.vars[node[1]] = self.walk(node[2])
        elif tag == 'print': print(self.walk(node[1]))
        elif tag == 'agent':
            self.agent_persona, self.agent_task = self.walk(node[1]), self.walk(node[2])
        elif tag == 'predict':
            if self.client:
                resp = self.client.models.generate_content(model="gemini-1.5-flash", contents=f"{self.agent_persona}: {self.walk(node[1])}")
                print(f"[AI]: {resp.text}")
        elif tag == 'serve':
            self.html_buffer = self.walk(node[1])
            app = Flask("NexusWeb")
            @app.route('/')
            def home(): return f"<html><head><script src='https://cdn.tailwindcss.com'></script></head><body>{self.html_buffer}</body></html>"
            threading.Thread(target=lambda: app.run(port=5000, host='127.0.0.1', use_reloader=False), daemon=True).start()
            time.sleep(1); webbrowser.open("http://127.0.0.1:5000")
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt: pass
        if tag in ('+', '-', '*', '/', '==', '<', '>'):
            l, r = self.walk(node[1]), self.walk(node[2])
            ops = {'+':l+r, '-':l-r, '*':l*r, '/':(l//r if r!=0 else 0), '==':l==r, '<':l<r, '>':l>r}
            return ops[tag]
