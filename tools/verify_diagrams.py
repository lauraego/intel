import asyncio, json, sys
from playwright.async_api import async_playwright
SL=["what-happens-at-the-end-of-a-debt-cycle","is-the-human-body-electrical","why-does-the-same-thing-keep-happening-to-me","scroll-scan-review"]
BASE=sys.argv[1] if len(sys.argv)>1 else "http://localhost:4931/blog/{}.html"
OUT="/Users/lauraegocheaga/.st-work/glennbeck-ads/intel/anim/"
CLS_JS="""window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries()){if(!e.hadRecentInput)window.__cls+=e.value}}).observe({type:'layout-shift',buffered:true});"""
STATE_JS="""f=>{const d=f.querySelector('.dg');const hid=[...d.querySelectorAll('.pop,.slide,.slider,.slam,.zoom')].filter(e=>getComputedStyle(e).opacity<0.5&&!e.classList.contains('dimmed')).length;
const undrawn=[...d.querySelectorAll('.draw')].filter(e=>parseFloat(getComputedStyle(e).strokeDashoffset)>0.01).length;
return {cls:d.className,hidden:hid,undrawn:undrawn,cnt:[...d.querySelectorAll('.cnt')].map(e=>e.textContent),anims:d.getAnimations({subtree:true}).length}}"""
async def run(p, mode):
    b=await p.chromium.launch()
    kw=dict(viewport={"width":420,"height":860},device_scale_factor=2)
    if mode=="reduced": kw["reduced_motion"]="reduce"
    if mode=="nojs": kw["java_script_enabled"]=False
    if mode=="video": kw.update(record_video_dir=OUT+"video",record_video_size={"width":420,"height":860},device_scale_factor=1)
    ctx=await b.new_context(**kw)
    res={}
    for s in SL:
        pg=await ctx.new_page()
        if mode!="nojs": await pg.add_init_script(CLS_JS)
        await pg.goto(BASE.format(s),wait_until="networkidle")
        figs=await pg.query_selector_all("figure.dgf")
        pre=[await f.evaluate(STATE_JS) for f in figs] if mode=="default" else None
        out=[]
        for i,f in enumerate(figs):
            if mode=="video":
                await pg.evaluate("y=>window.scrollTo({top:y,behavior:'smooth'})", await f.evaluate("f=>f.getBoundingClientRect().top+scrollY-200"))
                await pg.wait_for_timeout(5200); continue
            await f.scroll_into_view_if_needed()
            if mode=="default":
                await pg.wait_for_timeout(900); await f.screenshot(path=f"{OUT}mid/{s}-{i+1}.png")
                await pg.wait_for_timeout(4800)
                await f.screenshot(path=f"{OUT}after/{s}-{i+1}.png")
            else:
                await pg.wait_for_timeout(150); await f.screenshot(path=f"{OUT}{mode}/{s}-{i+1}.png")
            out.append(await f.evaluate(STATE_JS))
        cls=await pg.evaluate("window.__cls||0") if mode!="nojs" else None
        res[s]={"figs":len(figs),"pre_scroll":pre,"final":out,"cls":cls}
        await pg.close()
    await ctx.close(); await b.close()
    return res
async def main():
    async with async_playwright() as p:
        mode=sys.argv[2] if len(sys.argv)>2 else "default"
        r=await run(p,mode)
        print(json.dumps(r,indent=0)[:6000])
asyncio.run(main())
