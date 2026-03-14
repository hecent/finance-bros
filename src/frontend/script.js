async function fetchState() {
    const res = await fetch("/state");
    const state = await res.json();
    renderState(state);
}

const statHistory = {
    balance: [],
};

function setBalance(value) {
    const el = document.getElementById("balance");
    el.textContent = `£${value}`;
    el.classList.remove("positive", "negative", "neutral");

    if (value > 0) {
        el.classList.add("positive");
    } else if (value < 0) {
        el.classList.add("negative");
    } else {
        el.classList.add("neutral");
    }
}

function setGrade(value) {
    const el = document.getElementById("grades");
    el.textContent = value.toFixed(1);
    el.classList.remove("first", "two-one", "two-two", "third", "fail");

    if (value >= 16.5) {
        el.classList.add("first");
    } else if (value >= 13.5) {
        el.classList.add("two-one");
    } else if (value >= 10.5) {
        el.classList.add("two-two");
    } else if (value >= 7) {
        el.classList.add("third");
    } else {
        el.classList.add("fail");
    }
}

function updateHistory(state) {
    statHistory.balance.push(state.balance);
}

async function resetState() {
    const res = await fetch("/reset");
    const state = await res.json();
    renderState(state);
}

function renderState(state) {
    document.getElementById("year").textContent = `Year: ${state.year}`;
    document.getElementById("week").textContent = `Week: ${state.week}`;
    
    if (state.game_over === true) {
        let score = (state.happiness + state.balance + state.grades) / 100;
        alert(`Game over. Final Score: ${score.toFixed(2)}`);
        resetState();
        return;
    }

    // Handle Text Animation triggering
    const scenarioText = document.getElementById("scenario-text");
    scenarioText.classList.remove("animate-text");
    void scenarioText.offsetWidth; // Trigger DOM reflow to restart animation
    scenarioText.textContent = state.scenario;
    scenarioText.classList.add("animate-text");
    if (state.game_over === true) {
        let score = (state.happiness + state.balance + state.grades) / 100
        alert(`Game over. Score: ${score}`);
        resetState()
    }

    setBalance(state.balance);
    document.getElementById("happiness").textContent = state.happiness.toFixed(1);
    setGrade(state.grades);

    updateHistory(state);

    const choicesDiv = document.getElementById("choices");
    choicesDiv.innerHTML = "";

    // Render Buttons with staggered animation
    state.choices.forEach((option, index) => {
        const btn = document.createElement("button");
        btn.className = "choice-btn animate-btn";
        btn.textContent = option.text;
        // Stagger the animation delay so buttons cascade in
        btn.style.animationDelay = `${index * 0.1}s`; 
        btn.onclick = () => submitChoice(option.id);
        choicesDiv.appendChild(btn);
    });

    drawGraph(statHistory);
}

async function submitChoice(choiceId) {
    const res = await fetch("/choose", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ choice_id: choiceId })
    });

    const state = await res.json();
    renderState(state);
}

const canvas = document.getElementById("statsGraph");
const ctx = canvas.getContext("2d");

function drawGraph(history) {
    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;

    ctx.clearRect(0, 0, width, height);

    if (history.balance.length === 0) return;

    const minValue = Math.min(...history.balance, 0);
    const maxValue = Math.max(...history.balance, 0);
    const weekCount = history.balance.length;

    function xScale(i) {
        if (weekCount <= 1) return padding;
        return padding + (i / (weekCount - 1)) * (width - padding * 2);
    }

    function yScale(value) {
        return height - padding - ((value - minValue) / (maxValue - minValue || 1)) * (height - padding * 2);
    }

    // Clean up Graph Grid Styling
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 1;

    // Y axis
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.stroke();

    // X axis at y = 0
    const zeroY = yScale(0);
    ctx.beginPath();
    ctx.moveTo(padding, zeroY);
    ctx.lineTo(width - padding, zeroY);
    ctx.strokeStyle = "#9ca3af";
    ctx.stroke();

    // Y axis ticks and labels
    ctx.fillStyle = "#6b7280";
    ctx.font = "12px Inter, Arial";

    const tickCount = 5;
    for (let i = 0; i <= tickCount; i++) {
        const value = minValue + (i / tickCount) * (maxValue - minValue);
        const y = yScale(value);
        ctx.fillText(value.toFixed(0), padding - 35, y + 4);
    }

    // X-axis labels
    for (let i = 0; i < weekCount; i++) {
        const x = xScale(i);
        ctx.fillText(`W${i + 1}`, x - 10, height - padding + 20);
    }

    // Draw Line
    ctx.beginPath();
    ctx.strokeStyle = "#00539b";
    ctx.lineWidth = 3;

    history.balance.forEach((value, i) => {
        const x = xScale(i);
        const y = yScale(value);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Draw Points
    ctx.fillStyle = "#00539b";
    history.balance.forEach((value, i) => {
        const x = xScale(i);
        const y = yScale(value);
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 2;
        ctx.stroke();
    });
}

fetchState();