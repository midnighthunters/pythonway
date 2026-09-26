/**
 * American Express Travel Concierge & LangGraph Autonomous Engine Frontend
 * Handles dynamic state polling, HITL interrupt/resume, Amex mobile UI animations,
 * and Groq LLM Travel Concierge conversational streaming.
 */

// Global State References
let currentTravelState = null;
let currentActiveTab = 'home';
let isExpandedMode = false;

// DOM Elements
const btnSimulate = document.getElementById('btn-simulate-disruption');
const btnReset = document.getElementById('btn-reset-itinerary');
const btnToggleViewport = document.getElementById('btn-toggle-viewport');
const frameToggleLabel = document.getElementById('frame-toggle-label');
const viewportWrapper = document.getElementById('viewport-wrapper');

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  initMermaid();
  setupEventListeners();
  fetchState();
  fetchChatHistory();
});

function initMermaid() {
  if (window.mermaid) {
    window.mermaid.initialize({
      startOnLoad: true,
      theme: 'dark',
      themeVariables: {
        darkMode: true,
        background: '#0f172a',
        primaryColor: '#002663',
        primaryTextColor: '#ffffff',
        primaryBorderColor: '#3b82f6',
        lineColor: '#60a5fa',
        secondaryColor: '#1e293b',
        tertiaryColor: '#0f172a'
      }
    });
  }
}

function setupEventListeners() {
  btnSimulate.addEventListener('click', handleSimulateDisruption);
  btnReset.addEventListener('click', handleResetItinerary);
  btnToggleViewport.addEventListener('click', toggleViewportMode);
}

// ==============================================================================
// VIEWPORT EXPAND / MOBILE TOGGLE
// ==============================================================================
function toggleViewportMode() {
  isExpandedMode = !isExpandedMode;
  if (isExpandedMode) {
    viewportWrapper.classList.add('expanded-mode');
    frameToggleLabel.textContent = 'Phone Frame';
    btnToggleViewport.querySelector('i').className = 'fa-solid fa-mobile-screen-button';
  } else {
    viewportWrapper.classList.remove('expanded-mode');
    frameToggleLabel.textContent = 'Expand View';
    btnToggleViewport.querySelector('i').className = 'fa-solid fa-expand';
  }
}

// ==============================================================================
// TAB NAVIGATION
// ==============================================================================
function switchTab(tabName) {
  currentActiveTab = tabName;

  // Toggle Tab Panes
  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.remove('active');
  });
  const targetPane = document.getElementById(`tab-${tabName}`);
  if (targetPane) {
    targetPane.classList.add('active');
  }

  // Toggle Bottom Nav Items
  document.querySelectorAll('.nav-tab-item').forEach(btn => {
    btn.classList.remove('active');
  });
  const targetNavBtn = document.getElementById(`nav-btn-${tabName}`);
  if (targetNavBtn) {
    targetNavBtn.classList.add('active');
  }

  // If switching to Graph Live, trigger mermaid re-render
  if (tabName === 'graph' && window.mermaid) {
    window.mermaid.contentLoaded();
  }

  // Scroll to top of app screen
  const scrollContainer = document.getElementById('screen-container');
  if (scrollContainer) {
    scrollContainer.scrollTop = 0;
  }
}

// ==============================================================================
// STATE FETCHING & UI SYNCHRONIZATION
// ==============================================================================
async function fetchState() {
  try {
    const res = await fetch('/api/state');
    const state = await res.json();
    currentTravelState = state;
    renderUI(state);
  } catch (err) {
    console.error('Error fetching state:', err);
  }
}

function renderUI(state) {
  if (!state) return;

  const profile = state.user_profile || {};
  const itinerary = state.itinerary || {};
  const flight = itinerary.flight || {};
  const cab = itinerary.cab || {};
  const hotel = itinerary.hotel || {};
  const lounge = itinerary.lounge || {};
  const dinner = itinerary.dinner || {};
  const disruption = state.disruption;
  const impacts = state.impact_assessment || [];
  const policies = state.policy_benefits || [];
  const options = state.options || [];
  const receipts = state.rebooking_receipts || [];
  const workflowStatus = state.workflow_status || 'IDLE';

  // 1. User & Card Info
  document.getElementById('user-display-name').textContent = profile.name || 'Alexander V. Vance';
  document.getElementById('card-holder-text').textContent = (profile.name || 'Alexander V. Vance').toUpperCase();
  document.getElementById('card-embossed-num').textContent = `•••• •••• •••• ${profile.card_last4 || '84001'}`;
  document.getElementById('points-display').textContent = `${(profile.points_balance || 482910).toLocaleString()} pts`;
  document.getElementById('user-avatar').textContent = profile.avatar_initials || 'AV';

  // 2. Urgent Disruption Alert Banner
  const banner = document.getElementById('urgent-disruption-banner');
  const disruptionNavDot = document.getElementById('disruption-nav-dot');
  const notifDot = document.getElementById('notif-badge-dot');

  if (flight.status === 'CANCELLED' || state.hitl_interrupted) {
    banner.style.display = 'block';
    disruptionNavDot.style.display = 'block';
    notifDot.style.display = 'block';
  } else {
    banner.style.display = 'none';
    disruptionNavDot.style.display = 'none';
    notifDot.style.display = 'none';
  }

  // 3. Status Badges & Itinerary Details
  // Flight
  updateStatusBadge('flight-status-badge', flight.status, flight.status_color);
  document.getElementById('flight-origin-code').textContent = flight.origin || 'JFK';
  document.getElementById('flight-dest-code').textContent = flight.destination || 'LAX';
  document.getElementById('flight-dep-time').textContent = flight.scheduled_departure || '15:45 EST';
  document.getElementById('flight-seat-num').textContent = flight.seat || '2B';
  document.getElementById('flight-pnr-code').textContent = flight.pnr || 'AMX7X9';
  document.getElementById('flight-carrier-line').textContent = `${flight.flight_number || 'AA-1420'} • ${flight.airline || 'American Airlines'}`;

  // Card highlight for disrupted flight
  const flightCard = document.getElementById('flight-card-container');
  if (flight.status === 'CANCELLED') {
    flightCard.className = 'itinerary-item-card disrupted-card';
  } else if (flight.status === 'REBOOKED') {
    flightCard.className = 'itinerary-item-card rebooked-card';
  } else {
    flightCard.className = 'itinerary-item-card';
  }

  // Cab
  updateStatusBadge('cab-status-badge', cab.status, cab.status_color);
  document.getElementById('cab-service-name').textContent = cab.service_provider || 'Blacklane Chauffeur';
  document.getElementById('cab-car-model').textContent = `${cab.vehicle_model || 'Mercedes-Benz S-Class'} • Driver: ${cab.driver_name || 'Marcus Thorne'}`;
  document.getElementById('cab-pickup-time').textContent = cab.pickup_time || '19:40 PST';
  document.getElementById('cab-pickup-loc').textContent = cab.pickup_location ? cab.pickup_location.split('-')[0] : 'LAX Bradley';

  // Hotel
  updateStatusBadge('hotel-status-badge', hotel.status, hotel.status_color);
  document.getElementById('hotel-property-name').textContent = hotel.property_name || 'The Beverly Hills Hotel';
  document.getElementById('hotel-room-type').textContent = hotel.room_type || 'Bungalow Suite';
  document.getElementById('hotel-checkin-time').textContent = `${hotel.check_in_date || 'Today'}, ${hotel.scheduled_check_in_time || '20:30 PST'}`;
  document.getElementById('hotel-res-code').textContent = hotel.reservation_code || 'BHH-AMX-5519';

  // Lounge
  updateStatusBadge('lounge-status-badge', lounge.status, lounge.status_color);
  document.getElementById('lounge-name-text').textContent = lounge.lounge_name || 'The Centurion® Lounge';
  document.getElementById('lounge-terminal-text').textContent = `${lounge.terminal || 'Terminal 4'} • Access: ${lounge.valid_window || '13:00 - 15:45 EST'}`;
  document.getElementById('lounge-barcode-text').textContent = lounge.barcode_code || 'AMX-CENT-JFK-99824';

  // Dinner
  updateStatusBadge('dinner-status-badge', dinner.status, dinner.status_color);
  document.getElementById('dinner-restaurant-name').textContent = dinner.restaurant_name || 'Nobu Malibu';
  document.getElementById('dinner-table-type').textContent = `${dinner.table_type || 'Patio Terrace'} • ${dinner.guests || 2} Guests`;
  document.getElementById('dinner-time-text').textContent = dinner.reservation_time || '20:45 PST';

  // 4. Compact Itinerary on Home Screen
  renderHomeCompactItinerary(itinerary);

  // 5. Disruption Hub: Impact Assessment & Options
  renderDisruptionHub(state);

  // 6. Graph Live Tab
  renderGraphLiveTab(state);

  // 7. Raw State Inspector
  document.getElementById('raw-state-inspector').textContent = JSON.stringify(state, null, 2);
}

function updateStatusBadge(elementId, statusText, color) {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.textContent = (statusText || 'ON TIME').replace(/_/g, ' ');
  el.className = `status-badge ${color || 'green'}`;
}

// ==============================================================================
// RENDER COMPACT HOME ITINERARY
// ==============================================================================
function renderHomeCompactItinerary(itinerary) {
  const container = document.getElementById('home-compact-itinerary');
  if (!container) return;

  const items = [
    {
      icon: 'fa-plane',
      name: `${itinerary.flight?.airline || 'American Airlines'} ${itinerary.flight?.flight_number || 'AA-1420'}`,
      sub: `${itinerary.flight?.origin || 'JFK'} ➔ ${itinerary.flight?.destination || 'LAX'} • Dep: ${itinerary.flight?.scheduled_departure || '15:45 EST'}`,
      badge: (itinerary.flight?.status || 'ON_TIME').replace(/_/g, ' '),
      color: itinerary.flight?.status_color || 'green'
    },
    {
      icon: 'fa-car',
      name: itinerary.cab?.service_provider || 'Blacklane Executive Chauffeur',
      sub: `Pickup ${itinerary.cab?.pickup_time || '19:40 PST'} • Mercedes S-Class`,
      badge: (itinerary.cab?.status || 'CONFIRMED').replace(/_/g, ' '),
      color: itinerary.cab?.status_color || 'green'
    },
    {
      icon: 'fa-hotel',
      name: itinerary.hotel?.property_name || 'The Beverly Hills Hotel',
      sub: `Bungalow Suite • Check-in ${itinerary.hotel?.scheduled_check_in_time || '20:30 PST'}`,
      badge: (itinerary.hotel?.status || 'CONFIRMED').replace(/_/g, ' '),
      color: itinerary.hotel?.status_color || 'green'
    },
    {
      icon: 'fa-martini-glass',
      name: itinerary.lounge?.lounge_name || 'The Centurion® Lounge JFK',
      sub: `Access Window: ${itinerary.lounge?.valid_window || '13:00 - 15:45 EST'}`,
      badge: (itinerary.lounge?.status || 'ACTIVE').replace(/_/g, ' '),
      color: itinerary.lounge?.status_color || 'green'
    },
    {
      icon: 'fa-utensils',
      name: itinerary.dinner?.restaurant_name || 'Nobu Malibu',
      sub: `Table for 2 • ${itinerary.dinner?.reservation_time || '20:45 PST'}`,
      badge: (itinerary.dinner?.status || 'CONFIRMED').replace(/_/g, ' '),
      color: itinerary.dinner?.status_color || 'green'
    }
  ];

  container.innerHTML = items.map(item => `
    <div style="background: #ffffff; border-radius: 12px; padding: 12px 14px; border: 1px solid var(--amex-border); display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-sm);">
      <div style="display: flex; align-items: center; gap: 12px;">
        <div style="width: 32px; height: 32px; border-radius: 8px; background: #eff6ff; color: var(--amex-blue-primary); display: flex; align-items: center; justify-content: center; font-size: 13px;">
          <i class="fa-solid ${item.icon}"></i>
        </div>
        <div>
          <div style="font-size: 13px; font-weight: 700; color: var(--amex-text-dark);">${item.name}</div>
          <div style="font-size: 11px; color: var(--amex-text-muted);">${item.sub}</div>
        </div>
      </div>
      <span class="status-badge ${item.color}">${item.badge}</span>
    </div>
  `).join('');
}

// ==============================================================================
// RENDER DISRUPTION HUB & RECOVERY PACKAGES
// ==============================================================================
function renderDisruptionHub(state) {
  const impacts = state.impact_assessment || [];
  const policies = state.policy_benefits || [];
  const options = state.options || [];
  const receipts = state.rebooking_receipts || [];
  const totalExposure = state.total_financial_exposure || 0;
  const workflowStatus = state.workflow_status || 'IDLE';

  document.getElementById('disruption-hub-badge').textContent = `STATUS: ${workflowStatus}`;
  document.getElementById('exposure-amount-pill').textContent = `Exposure: $${totalExposure.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;

  // 1. Render Cascaded Impacts List
  const impactContainer = document.getElementById('impact-items-list');
  if (impacts.length === 0) {
    impactContainer.innerHTML = `
      <div style="font-size: 12px; color: #64748b; padding: 14px 0; text-align: center;">
        <i class="fa-solid fa-circle-check" style="color: #059669; font-size: 20px; margin-bottom: 6px; display: block;"></i>
        All 5 travel services operating smoothly. Tap <b>"Simulate AA-1420 Cancellation"</b> in the top bar to test autonomous disruption mitigation.
      </div>
    `;
  } else {
    const iconMap = { cab: 'fa-car', hotel: 'fa-hotel', lounge: 'fa-martini-glass', dinner: 'fa-utensils', flight: 'fa-plane' };
    impactContainer.innerHTML = impacts.map(imp => `
      <div class="impact-row-item">
        <div class="impact-icon-col">
          <i class="fa-solid ${iconMap[imp.service] || 'fa-triangle-exclamation'}"></i>
        </div>
        <div class="impact-details-col">
          <div style="display: flex; justify-content: space-between;">
            <span class="impact-title-line">${imp.title}</span>
            <span class="impact-exposure-tag">$${imp.risk_amount.toFixed(2)} Risk</span>
          </div>
          <div class="impact-desc-line">${imp.description}</div>
          <div style="font-size: 10px; color: #0070d1; font-weight: 600; margin-top: 2px;">
            <i class="fa-solid fa-wrench"></i> ${imp.proposed_remedy}
          </div>
        </div>
      </div>
    `).join('');
  }

  // 2. Render Policy Box
  const policyBox = document.getElementById('policy-box');
  const policyContainer = document.getElementById('policy-items-list');
  if (policies.length > 0) {
    policyBox.style.display = 'block';
    policyContainer.innerHTML = policies.map(pol => `
      <div style="background: #f8fafc; border-radius: 8px; padding: 8px 10px; border-left: 3px solid var(--amex-gold); display: flex; flex-direction: column; gap: 2px;">
        <div style="font-size: 12px; font-weight: 700; color: var(--amex-navy);">
          <i class="fa-solid fa-shield-check" style="color: var(--amex-gold);"></i> ${pol.benefit_name}
        </div>
        <div style="font-size: 11px; color: #475569;">${pol.details}</div>
      </div>
    `).join('');
  } else {
    policyBox.style.display = 'none';
  }

  // 3. Render Multi-Modal Recovery Packages (Options)
  const optionsHeader = document.getElementById('options-header');
  const optionsContainer = document.getElementById('options-container');

  if (options.length > 0 && (state.hitl_interrupted || workflowStatus === 'AWAITING_USER_APPROVAL')) {
    optionsHeader.style.display = 'flex';
    optionsContainer.innerHTML = options.map((opt, idx) => `
      <div class="option-card ${idx === 0 ? 'selected-option' : ''}" id="card-${opt.id}">
        <div class="option-top-badge ${opt.badge_color}">${opt.badge}</div>
        <div class="option-title-text">${opt.title}</div>
        <div class="option-summary-text">${opt.summary}</div>

        <div class="option-metrics-grid">
          <div>
            <div class="metric-col-title">Delay / ETA</div>
            <div class="metric-col-val">${opt.eta_impact}</div>
          </div>
          <div>
            <div class="metric-col-title">Cost Delta</div>
            <div class="metric-col-val">${opt.cost_delta.split(' ')[0]}</div>
          </div>
          <div>
            <div class="metric-col-title">Goodwill Bonus</div>
            <div class="metric-col-val" style="color: #059669;">${opt.points_bonus.split(' ')[0]}</div>
          </div>
        </div>

        <div class="option-sync-bullets">
          <div class="option-sync-item">
            <i class="fa-solid fa-plane" style="color: #0070d1; width: 14px;"></i>
            <span><b>Flight:</b> ${opt.flight_plan.carrier} ${opt.flight_plan.flight_number} (${opt.flight_plan.departure} ➔ ${opt.flight_plan.arrival}) [${opt.flight_plan.cabin}]</span>
          </div>
          <div class="option-sync-item">
            <i class="fa-solid fa-car" style="color: #0070d1; width: 14px;"></i>
            <span><b>Chauffeur:</b> ${opt.cab_plan.note}</span>
          </div>
          <div class="option-sync-item">
            <i class="fa-solid fa-hotel" style="color: #0070d1; width: 14px;"></i>
            <span><b>Hotel:</b> ${opt.hotel_plan.note}</span>
          </div>
          <div class="option-sync-item">
            <i class="fa-solid fa-martini-glass" style="color: #0070d1; width: 14px;"></i>
            <span><b>Lounge:</b> ${opt.lounge_plan.note}</span>
          </div>
          <div class="option-sync-item">
            <i class="fa-solid fa-utensils" style="color: #0070d1; width: 14px;"></i>
            <span><b>Dinner:</b> ${opt.dinner_plan.note}</span>
          </div>
        </div>

        <button class="btn-approve-option" onclick="handleResumeOption('${opt.id}')">
          <i class="fa-solid fa-check"></i>
          <span>Approve & Re-Synchronize Entire Trip (${opt.id.replace('opt_', '').toUpperCase()})</span>
        </button>
      </div>
    `).join('');
  } else {
    optionsHeader.style.display = 'none';
    optionsContainer.innerHTML = '';
  }

  // 4. Render Rebooking Receipts (When resolved)
  const receiptsBox = document.getElementById('rebooking-receipt-box');
  const receiptsList = document.getElementById('receipt-items-list');

  if (receipts.length > 0 && workflowStatus === 'RESOLVED') {
    receiptsBox.style.display = 'block';
    receiptsList.innerHTML = receipts.map(r => `
      <div style="padding: 6px 0; border-bottom: 1px dashed #e2e8f0; display: flex; justify-content: space-between;">
        <span style="font-weight: 700; text-transform: uppercase;">${r.service}:</span>
        <span style="font-family: monospace; color: #059669;">${JSON.stringify(r.result).substring(0, 55)}...</span>
      </div>
    `).join('') + `
      <div style="margin-top: 10px; font-weight: 700; color: #002663;">
        🎉 All 5 services synchronized with \$0 fee penalty. +10,000 Membership Rewards points credited.
      </div>
    `;
  } else {
    receiptsBox.style.display = 'none';
  }
}

// ==============================================================================
// RENDER GRAPH LIVE TAB (LANGGRAPH ARCHITECTURE & TELEMETRY)
// ==============================================================================
function renderGraphLiveTab(state) {
  const activeNode = state.active_node || 'idle';
  const workflowStatus = state.workflow_status || 'IDLE';

  document.getElementById('graph-live-status-pill').textContent = `ACTIVE: ${activeNode.toUpperCase()}`;

  const nodes = [
    { id: 'itinerary_monitor_node', step: '1', name: 'Itinerary Monitor Node', desc: 'Flight Telemetry Ingestion & Disruption Detection' },
    { id: 'downstream_impact_node', step: '2', name: 'Downstream Impact Node', desc: 'Spatial & Temporal Cascade Assessment (Cab, Hotel, Lounge, Dining)' },
    { id: 'amex_policy_node', step: '3', name: 'Amex Policy & Benefits Node', desc: 'Centurion Protections, Fine Hotels & Resorts Arrival Holds' },
    { id: 'option_generator_node', step: '4', name: 'Option Generator Node', desc: 'Synthesizes 3 Multi-Modal Full-Trip Recovery Packages' },
    { id: 'human_in_the_loop_node', step: '5', name: 'Human-in-the-Loop Node', desc: 'LangGraph Native interrupt() Breakpoint for Cardmember Choice' },
    { id: 'rebooking_orchestrator_node', step: '6', name: 'Rebooking Orchestrator Node', desc: 'Atomic Multi-API Dispatch (GDS, Blacklane, FHR, Resy)' },
    { id: 'notification_synthesizer_node', step: '7', name: 'Notification Synthesizer Node', desc: 'Amex Push Notifications, Boarding Pass & Apple Wallet Sync' },
    { id: 'audit_telemetry_node', step: '8', name: 'Audit & Telemetry Node', desc: 'Loss Avoidance Analytics ($2,390 Protected) & Checkpoint Commit' }
  ];

  const listContainer = document.getElementById('nodes-timeline-list');
  if (!listContainer) return;

  listContainer.innerHTML = nodes.map(n => {
    let nodeClass = '';
    let statusLabel = 'PENDING';

    if (activeNode === n.id) {
      nodeClass = (n.id === 'human_in_the_loop_node' && state.hitl_interrupted) ? 'paused-node' : 'active-node';
      statusLabel = (n.id === 'human_in_the_loop_node' && state.hitl_interrupted) ? '⏸️ PAUSED (INTERRUPT)' : '⚡ RUNNING';
    } else if (workflowStatus === 'RESOLVED') {
      nodeClass = 'completed-node';
      statusLabel = '✓ COMPLETED';
    } else if (state.hitl_interrupted && parseInt(n.step) <= 5) {
      nodeClass = (parseInt(n.step) === 5) ? 'paused-node' : 'completed-node';
      statusLabel = (parseInt(n.step) === 5) ? '⏸️ PAUSED (INTERRUPT)' : '✓ COMPLETED';
    }

    return `
      <div class="graph-node-card ${nodeClass}">
        <div class="node-left-meta">
          <div class="node-step-circle">${n.step}</div>
          <div>
            <div class="node-name-text">${n.name}</div>
            <div class="node-desc-text">${n.desc}</div>
          </div>
        </div>
        <span style="font-size: 10px; font-weight: 800; letter-spacing: 0.5px;">${statusLabel}</span>
      </div>
    `;
  }).join('');
}

// ==============================================================================
// LANGGRAPH ACTIONS: SIMULATE & RESUME
// ==============================================================================
async function handleSimulateDisruption() {
  btnSimulate.disabled = true;
  btnSimulate.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Running LangGraph...</span>';

  try {
    const res = await fetch('/api/disruption/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        flight_number: 'AA-1420',
        reason: 'Severe convective storm cluster & FAA ground stop at New York JFK',
        event_type: 'FLIGHT_CANCELLATION'
      })
    });

    const data = await res.json();
    currentTravelState = data.state;
    renderUI(data.state);

    // Switch to Disruption Hub tab automatically
    switchTab('disruption');
    fetchChatHistory();

  } catch (err) {
    console.error('Error simulating disruption:', err);
    alert('Failed to simulate flight disruption.');
  } finally {
    btnSimulate.disabled = false;
    btnSimulate.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> <span>Simulate AA-1420 Cancellation</span>';
  }
}

async function handleResumeOption(selectedOptionId) {
  const card = document.getElementById(`card-${selectedOptionId}`);
  if (card) {
    const btn = card.querySelector('.btn-approve-option');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Synchronizing Services...</span>';
    }
  }

  try {
    const res = await fetch('/api/disruption/resume', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        selected_option_id: selectedOptionId,
        user_notes: `Approved ${selectedOptionId} via Amex Mobile App`
      })
    });

    const data = await res.json();
    currentTravelState = data.state;
    renderUI(data.state);
    fetchChatHistory();

  } catch (err) {
    console.error('Error resuming option:', err);
    alert('Failed to rebook itinerary.');
  }
}

async function handleResetItinerary() {
  try {
    const res = await fetch('/api/reset', { method: 'POST' });
    const data = await res.json();
    currentTravelState = data.state;
    renderUI(data.state);
    switchTab('home');
    fetchChatHistory();
  } catch (err) {
    console.error('Error resetting:', err);
  }
}

// ==============================================================================
// AMEX CONCIERGE CHAT ENGINE
// ==============================================================================
async function fetchChatHistory() {
  try {
    const res = await fetch('/api/chat/history');
    const data = await res.json();
    renderChatMessages(data.history || []);
  } catch (err) {
    console.error('Error fetching chat:', err);
  }
}

function renderChatMessages(history) {
  const container = document.getElementById('chat-stream');
  if (!container) return;

  container.innerHTML = history.map(msg => `
    <div class="chat-bubble ${msg.role === 'user' ? 'user' : 'assistant'}">
      ${formatMarkdownText(msg.content)}
    </div>
  `).join('');

  container.scrollTop = container.scrollHeight;
}

function formatMarkdownText(text) {
  if (!text) return '';
  return text
    .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
    .replace(/\*(.*?)\*/g, '<i>$1</i>')
    .replace(/\n/g, '<br>');
}

async function handleChatSubmit(event) {
  event.preventDefault();
  const input = document.getElementById('chat-input');
  const message = input.value.trim();
  if (!message) return;

  input.value = '';
  const sendBtn = document.getElementById('chat-send-btn');
  sendBtn.disabled = true;

  // Append user message immediately
  const container = document.getElementById('chat-stream');
  const tempUserBubble = document.createElement('div');
  tempUserBubble.className = 'chat-bubble user';
  tempUserBubble.textContent = message;
  container.appendChild(tempUserBubble);

  const tempAssistantBubble = document.createElement('div');
  tempAssistantBubble.className = 'chat-bubble assistant';
  tempAssistantBubble.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Concierge consulting graph state...';
  container.appendChild(tempAssistantBubble);
  container.scrollTop = container.scrollHeight;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message })
    });

    const data = await res.json();
    renderChatMessages(data.chat_history || []);
  } catch (err) {
    console.error('Error in chat:', err);
    tempAssistantBubble.textContent = 'I apologize, Mr. Vance. An error occurred while consulting our systems.';
  } finally {
    sendBtn.disabled = false;
  }
}

function sendQuickChat(query) {
  document.getElementById('chat-input').value = query;
  const form = document.getElementById('chat-form');
  if (form) {
    form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
  }
}
