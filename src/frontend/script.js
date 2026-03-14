async function fetchState() {
    const res = await fetch("/state");
    const state = await res.json();
    renderState(state);
}

const statHistory = {
    balance: [],
    happiness: [],
    grades: []
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
    statHistory.happiness.push(state.happiness);
    statHistory.grades.push(state.grades);
}

function renderState(state) {
    document.getElementById("year").textContent = `Year: ${state.year}`;
    document.getElementById("week").textContent = `Week: ${state.week}`;
    document.getElementById("scenario-text").textContent = state.scenario;
    if (state.game_over === true) {
        let score = (state.happiness + state.balance + state.grades) / 100
        alert(`Game over. Score: ${score}`);
    }

    setBalance(state.balance);
    document.getElementById("happiness").textContent = state.happiness.toFixed(1);
    setGrade(state.grades);

    updateHistory(state);

    const choicesDiv = document.getElementById("choices");
    choicesDiv.innerHTML = "";

    state.choices.forEach(option => {
        const btn = document.createElement("button");
        btn.className = "choice-btn";
        btn.textContent = option.text;
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

    const allValues = [
        ...history.balance,
        ...history.happiness,
        ...history.grades
    ];

    if (allValues.length === 0) return;

    const minValue = Math.min(...allValues);
    const maxValue = Math.max(...allValues);
    const weekCount = Math.max(
        history.balance.length,
        history.happiness.length,
        history.grades.length
    );

    function xScale(i) {
        if (weekCount <= 1) return padding;
        return padding + (i / (weekCount - 1)) * (width - padding * 2);
    }

    function yScale(value) {
        return height - padding - ((value - minValue) / (maxValue - minValue || 1)) * (height - padding * 2);
    }

    function drawLine(data, color, label, labelY) {
        if (data.length === 0) return;

        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;

        data.forEach((value, i) => {
            const x = xScale(i);
            const y = yScale(value);

            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });

        ctx.stroke();

        ctx.fillStyle = color;
        data.forEach((value, i) => {
            const x = xScale(i);
            const y = yScale(value);

            ctx.beginPath();
            ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fill();
        });

        ctx.fillText(label, width - 100, labelY);
    }

    // axes
    ctx.strokeStyle = "#333";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();

    // x-axis labels
    ctx.fillStyle = "#333";
    ctx.font = "12px Arial";
    for (let i = 0; i < weekCount; i++) {
        const x = xScale(i);
        ctx.fillText(`W${i + 1}`, x - 10, height - padding + 20);
    }

    drawLine(history.balance, "#2e86de", "Balance", 20);
    drawLine(history.happiness, "#e67e22", "Happiness", 40);
    drawLine(history.grades, "#27ae60", "Grades", 60);
}

fetchState();