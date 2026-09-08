PLAYGROUND_HTML = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Safe Agent Playground</title>
  <style>
    :root { color-scheme: dark; --bg:#08111f; --panel:#0d1b2d; --line:#20324a; --text:#e8eef7; --muted:#9fb0c5; --accent:#68a7ff; --good:#63d7a0; --bad:#ff7f91; }
    * { box-sizing:border-box; }
    body { margin:0; font:15px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; background:radial-gradient(circle at 15% 0%,#17325a 0,transparent 38%),var(--bg); color:var(--text); }
    a { color:var(--accent); }
    .wrap { max-width:1120px; margin:0 auto; padding:40px 20px 72px; }
    .hero { display:grid; grid-template-columns:1.35fr .65fr; gap:24px; align-items:start; margin-bottom:24px; }
    .eyebrow { text-transform:uppercase; letter-spacing:.14em; color:var(--accent); font-weight:700; font-size:12px; }
    h1 { font-size:clamp(34px,6vw,64px); line-height:1; margin:10px 0 16px; letter-spacing:-.04em; }
    .lead { color:var(--muted); max-width:760px; font-size:17px; }
    .premise { margin-top:18px; border:1px solid #315b91; background:rgba(10,28,49,.9); border-radius:14px; padding:16px; }
    .premise strong { display:block; margin-bottom:7px; font-size:15px; }
    .premise p { margin:0; color:#d7e3f2; }
    .example { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:12px; }
    .example > div { border:1px solid var(--line); border-radius:10px; padding:11px 12px; background:#091523; }
    .example small { display:block; color:var(--muted); margin-bottom:4px; font-weight:700; text-transform:uppercase; letter-spacing:.06em; }
    .unsafe { color:var(--bad); }
    .safe { color:var(--good); }
    .flow { border:1px solid var(--line); background:rgba(13,27,45,.82); border-radius:18px; padding:18px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; color:#c9d8ea; }
    .grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
    .card { border:1px solid var(--line); background:rgba(13,27,45,.9); border-radius:18px; padding:20px; box-shadow:0 18px 60px rgba(0,0,0,.18); }
    h2 { margin:0 0 14px; font-size:18px; }
    label { display:block; margin:13px 0 6px; color:var(--muted); font-size:13px; font-weight:600; }
    input,select { width:100%; border:1px solid #29415f; background:#071321; color:var(--text); border-radius:10px; padding:11px 12px; outline:none; }
    input:focus,select:focus { border-color:var(--accent); box-shadow:0 0 0 3px rgba(104,167,255,.12); }
    .check { display:flex; gap:10px; align-items:center; margin:14px 0; color:var(--muted); }
    .check input { width:auto; }
    button { border:1px solid #315b91; background:#173a64; color:#fff; border-radius:10px; padding:10px 13px; cursor:pointer; font-weight:700; }
    button:hover { background:#214b7f; }
    button.secondary { background:#0b1929; border-color:var(--line); color:#c8d5e5; font-weight:600; }
    .actions { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
    .status { display:inline-flex; align-items:center; gap:8px; padding:6px 10px; border-radius:999px; background:#10243a; color:var(--muted); font-size:12px; }
    .dot { width:8px; height:8px; border-radius:50%; background:#8394aa; }
    .status.ok .dot { background:var(--good); box-shadow:0 0 0 4px rgba(99,215,160,.08); }
    .result-summary { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:14px 0; }
    .metric { border:1px solid var(--line); border-radius:12px; padding:12px; background:#091523; }
    .metric small { color:var(--muted); display:block; }
    .metric strong { font-size:17px; }
    pre { white-space:pre-wrap; overflow-wrap:anywhere; background:#06101d; border:1px solid var(--line); border-radius:12px; padding:14px; color:#cfe1f7; min-height:230px; margin:0; }
    .reason-good { color:var(--good); }
    .reason-bad { color:var(--bad); }
    .footer { color:var(--muted); margin-top:22px; font-size:13px; }
    @media (max-width:820px) { .hero,.grid,.example { grid-template-columns:1fr; } .result-summary { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <div>
        <div class="eyebrow">Open-source production safety demo</div>
        <h1>Safe Agent Playground</h1>
        <p class="lead"><strong>What problem does this solve?</strong> AI agents can suggest actions such as reading customer data or sending a notification. The dangerous design is letting the AI decide its own permissions. This demo shows the safer split: the AI proposes; the application decides whether the action is allowed.</p>

        <div class="premise" aria-label="Unsafe versus safe agent authorization example">
          <strong>The premise in one sentence</strong>
          <p><b>Model suggestion is not authorization.</b> A tool call must pass deterministic application policy before anything executes.</p>
          <div class="example">
            <div><small>Unsafe</small><span class="unsafe">AI says “send it” → tool executes because the model requested it.</span></div>
            <div><small>Safer</small><span class="safe">AI says “send it” → app checks tenant + policy + approval → executes or denies.</span></div>
          </div>
        </div>
      </div>
      <div class="flow">AI proposes action<br>↓<br><b>app policy checks scope</b><br>↓<br><b>human approval when required</b><br>↓<br><b>execute or deny</b><br>↓<br><b>audit records why</b></div>
    </section>

    <section class="grid">
      <div class="card">
        <div class="status" id="healthStatus"><span class="dot"></span><span>checking API…</span></div>
        <h2 style="margin-top:16px">Run a decision</h2>
        <form id="demoForm">
          <label for="actorTenant">Actor tenant</label>
          <input id="actorTenant" value="alpha" maxlength="64" required />

          <label for="resourceTenant">Resource tenant</label>
          <input id="resourceTenant" value="alpha" maxlength="64" required />

          <label for="tool">Tool</label>
          <select id="tool">
            <option value="read_record">read_record</option>
            <option value="send_notification">send_notification</option>
            <option value="delete_record">delete_record</option>
          </select>

          <label class="check"><input id="humanApproved" type="checkbox" /> Human approved</label>
          <button type="submit">Run policy + execution</button>
        </form>

        <div class="actions" aria-label="Example scenarios">
          <button class="secondary" data-scenario="read" type="button">Allowed read</button>
          <button class="secondary" data-scenario="cross" type="button">Cross-tenant deny</button>
          <button class="secondary" data-scenario="approval" type="button">Needs approval</button>
          <button class="secondary" data-scenario="approved" type="button">Approved action</button>
          <button class="secondary" data-scenario="delete" type="button">Blocked delete</button>
        </div>
      </div>

      <div class="card">
        <h2>Decision result</h2>
        <div class="result-summary">
          <div class="metric"><small>Allowed</small><strong id="allowed">—</strong></div>
          <div class="metric"><small>Executed</small><strong id="executed">—</strong></div>
          <div class="metric"><small>Reason</small><strong id="reason">—</strong></div>
        </div>
        <pre id="output" aria-live="polite">Choose a scenario or run the form.</pre>
      </div>
    </section>

    <p class="footer">Developer API: <a href="/docs">OpenAPI / Swagger</a> · Health: <a href="/health">/health</a> · Source: <a href="https://github.com/Videirafo/AI-Agent-Production-Checklist">GitHub</a></p>
  </main>

  <script>
    const $ = (id) => document.getElementById(id);
    const healthStatus = $('healthStatus');
    const form = $('demoForm');

    function requestId() {
      if (globalThis.crypto && crypto.randomUUID) return crypto.randomUUID();
      return `demo-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    }

    async function checkHealth() {
      try {
        const res = await fetch('/health', { cache: 'no-store' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        healthStatus.classList.add('ok');
        healthStatus.querySelector('span:last-child').textContent = 'API online';
      } catch (error) {
        healthStatus.querySelector('span:last-child').textContent = 'API unavailable';
      }
    }

    function applyScenario(name) {
      $('actorTenant').value = 'alpha';
      $('resourceTenant').value = name === 'cross' ? 'beta' : 'alpha';
      $('tool').value = name === 'delete' ? 'delete_record' : (name === 'approval' || name === 'approved' ? 'send_notification' : 'read_record');
      $('humanApproved').checked = name === 'approved' || name === 'delete';
    }

    async function runDemo() {
      const payload = {
        request_id: requestId(),
        actor_tenant_id: $('actorTenant').value.trim(),
        resource_tenant_id: $('resourceTenant').value.trim(),
        tool: $('tool').value,
        human_approved: $('humanApproved').checked,
      };

      $('output').textContent = 'Running…';
      try {
        const res = await fetch('/v1/run-demo', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const body = await res.json();
        if (!res.ok) throw new Error(JSON.stringify(body));

        $('allowed').textContent = String(body.decision.allowed);
        $('executed').textContent = String(body.executed);
        $('reason').textContent = body.decision.reason;
        $('reason').className = body.decision.allowed ? 'reason-good' : 'reason-bad';
        $('output').textContent = JSON.stringify(body, null, 2);
      } catch (error) {
        $('allowed').textContent = 'error';
        $('executed').textContent = 'false';
        $('reason').textContent = 'request_failed';
        $('reason').className = 'reason-bad';
        $('output').textContent = String(error);
      }
    }

    form.addEventListener('submit', (event) => { event.preventDefault(); runDemo(); });
    document.querySelectorAll('[data-scenario]').forEach((button) => {
      button.addEventListener('click', () => { applyScenario(button.dataset.scenario); runDemo(); });
    });

    checkHealth();
  </script>
</body>
</html>
'''
