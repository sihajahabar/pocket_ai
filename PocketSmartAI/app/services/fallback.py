from urllib.parse import quote_plus
def link(platform,q):
    q=quote_plus(q)
    return {"Amazon":f"https://www.amazon.in/s?k={q}","Flipkart":f"https://www.flipkart.com/search?q={q}",
    "IKEA":f"https://www.ikea.com/in/en/search/?q={q}","Swiggy":f"https://www.swiggy.com/search?query={q}",
    "Zomato":f"https://www.zomato.com/search?query={q}","OYO":f"https://www.oyorooms.com/search?location={q}"}.get(platform,f"https://www.google.com/search?q={q}")

def home(d):
    b=d["budget"]; a={"Furniture":b*.42,"Lighting":b*.15,"Decor":b*.18,"Storage":b*.15,"Contingency":b*.10}
    items=[("Furniture","Compact modular furniture set","IKEA",a["Furniture"]*.7,"space-saving furniture"),
           ("Lighting","Warm LED ceiling light","Amazon",a["Lighting"]*.7,"warm lighting"),
           ("Decor",d["style"]+" wall decor set","Amazon",a["Decor"]*.5,"style match"),
           ("Storage","Multipurpose organizer","Flipkart",a["Storage"]*.7,"practical storage")]
    return result("home",b,a,items,["Compare seller price, delivery and return policy.","Keep contingency for price changes."])
def party(d):
    b=d["budget"]; a={"Food":b*.50,"Decoration":b*.15,"Venue":b*.25,"Entertainment":b*.10}
    items=[("Food",f"Catering for {d['guests']} guests","Swiggy",a["Food"],"guest-count based"),
           ("Food","Restaurant/catering alternatives","Zomato",a["Food"]*.8,"comparison"),
           ("Venue",d["event_type"]+" venue options","OYO",a["Venue"],"venue search"),
           ("Decoration","Event decoration package","Amazon",a["Decoration"],"budget decor")]
    return result("party",b,a,items,["Confirm per-person fees and service charges.","Keep venue and food quotes separate."])
def jewelry(d):
    b=d["budget"]; a={"Necklace/Earrings":b*.55,"Bangles":b*.20,"Hair/Accessories":b*.10,"Contingency":b*.15}
    q=f"{d['style']} jewelry {d['occasion']} {d['outfit_color']}"
    items=[("Necklace/Earrings",d["style"]+" jewelry set","Amazon",a["Necklace/Earrings"],"occasion/style match"),
           ("Bangles","Matching bangle set","Flipkart",a["Bangles"],"coordinates with style")]
    return result("jewelry",b,a,items,["Use outfit color as a coordination cue.","Verify material, size and return policy."])
def result(planner,b,a,items,tips):
    return {"planner":planner,"budget":b,"allocation":{k:round(v,2) for k,v in a.items()},
    "items":[{"category":c,"name":n,"platform":p,"estimated_price":round(v,2),"quantity":1,"reason":r,"search_url":link(p,n)} for c,n,p,v,r in items],
    "tips":tips,"source":"local-fallback"}
