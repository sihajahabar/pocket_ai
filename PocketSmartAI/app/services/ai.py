import json
from google import genai
from google.genai import types
from app.config import settings
from app.services.fallback import home,party,jewelry

def generate(planner,data,image=None,mime=None):
    s=settings()
    fallback={"home":home,"party":party,"jewelry":jewelry}[planner](data)
    if not s.gemini_api_key: return fallback
    prompt='''You are PocketSmart AI. Return ONLY valid JSON.
Never claim live inventory or current prices. Estimated prices must be estimates.
Keep recommendations within the user's total budget.
Schema: {"planner":string,"budget":number,"allocation":object,"items":[
{"category":string,"name":string,"platform":string,"estimated_price":number,
"quantity":integer,"reason":string}],"tips":[string],"source":"gemini"}
Planner: '''+planner+"\nInput: "+json.dumps(data)
    try:
        c=genai.Client(api_key=s.gemini_api_key)
        parts=[prompt]
        if image: parts.append(types.Part.from_bytes(data=image,mime_type=mime or "image/jpeg"))
        r=c.models.generate_content(model=s.gemini_model,contents=parts,
            config=types.GenerateContentConfig(temperature=.3,response_mime_type="application/json"))
        x=json.loads(r.text); x["source"]="gemini"
        return x
    except Exception:
        return fallback
