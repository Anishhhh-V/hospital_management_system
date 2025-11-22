async function fetchAlerts(){
  try{
    const resp = await fetch('/api/alerts');
    if(!resp.ok) return;
    const alerts = await resp.json();
    const list = document.getElementById('alerts-list');
    const badge = document.getElementById('alert-count');
    if(!list || !badge) return;
    list.innerHTML = '';
    badge.textContent = alerts.length;
    alerts.forEach(a => {
      const li = document.createElement('li');
      li.className = 'list-group-item';
      li.innerHTML = `<strong>${a.alert_type}</strong> — ${a.message} <br/><small>${a.created_at}</small>`;
      list.appendChild(li);
    });
  } catch(e){
    console.error(e);
  }
}

setInterval(fetchAlerts, 5000);
window.onload = fetchAlerts;
