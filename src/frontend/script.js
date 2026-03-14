async function fetchState() {
    const res = await fetch("/state");
    const state = await res.json();
    renderState(state);
}

function renderState(state) {
    document.getElementById("year").textContent = `Year: ${state.year}`;
    document.getElementById("week").textContent = `Week: ${state.week}`;
    document.getElementById("scenario-text").textContent = state.scenario;

    document.getElementById("balance").textContent = `£${state.balance}`;
    document.getElementById("happiness").textContent = state.happiness;
    document.getElementById("grades").textContent = state.grades;

    const choicesDiv = document.getElementById("choices");
    choicesDiv.innerHTML = "";

    state.choices.forEach(choice => {
        const btn = document.createElement("button");
        btn.className = "choice-btn";
        btn.textContent = choice.text;
        btn.onclick = () => submitChoice(choice.id);
        choicesDiv.appendChild(btn);
    });
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

fetchState();