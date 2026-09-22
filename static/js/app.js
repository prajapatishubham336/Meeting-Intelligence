const demo = `Weekly Product Development Meeting.

Sarah: Good morning everyone. Let's discuss the progress of Project Alpha.

Rahul: The backend development is currently 80% complete.

Rahul: I will complete the remaining backend modules by Wednesday.

Priya: Once the backend is completed and approved, I will start testing on Thursday.

Amit: I will complete the payment API before testing begins.

Sarah: So, backend completion is a prerequisite for testing, and the payment API must also be ready before the testing phase.

Priya: I will prepare the test cases by Thursday morning and share the testing report with the team.

Rahul: If I face any technical issues, the backend delivery may be delayed.

Sarah: A backend delay could impact testing and the product launch scheduled for Friday.`;


// LOAD DEMO
function loadDemo() {
    const textarea = document.getElementById("transcriptText");
    textarea.value = demo;
    analyzeMeeting();
}


// ANALYZE MEETING
async function analyzeMeeting() {
    const textarea = document.getElementById("transcriptText");
    const text = textarea.value.trim();
    if (!text) {
        alert("Please paste a transcript first.");
        return;
    }

    const button = document.querySelector(".primary-btn");
    const originalButton = button.innerHTML;
    button.disabled = true;
    button.textContent = "Analyzing...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Backend analysis failed.");
        }

        renderResults(data);
    } catch (error) {
        console.error("Analysis Error:", error);
        alert(
            "Could not analyze transcript.\n\n" +
            error.message
        );
    } finally {
        button.disabled = false;
        button.innerHTML = originalButton;
        if (window.lucide) {
            lucide.createIcons();
        }
    }
}


// RENDER ALL RESULTS
function renderResults(data) {
    const stats = data.stats || {};

    // STATISTICS
    document.getElementById("decisionCount").textContent =
        stats.decisions || 0;

    document.getElementById("actionCount").textContent =
        stats.actions || 0;

    document.getElementById("dependencyCount").textContent =
        stats.dependencies || 0;

    document.getElementById("riskCount").textContent =
        stats.risks || 0;

    // SUMMARY
    const summary = document.getElementById("summary");
    summary.classList.remove("empty-state");
    const decisions = data.decisions || [];
    summary.innerHTML = `
        <div class="summary-result">
            <p>${escapeHTML(data.summary || "")}</p>
            ${
                decisions.length
                    ? `
                        <h4>Key Decisions</h4>
                        <ul>
                            ${decisions.map(decision => `
                                <li>
                                    ${escapeHTML(
                                        typeof decision === "object"
                                            ? decision.text
                                            : decision
                                    )}
                                </li>
                            `).join("")}
                        </ul>
                    `
                    : ""
            }
        </div>
    `;

    // ACTION ITEMS
    const actionsList = document.getElementById("actionsList");
    const actions = data.actions || [];
    actionsList.classList.remove("empty");
    if (!actions.length) {
        actionsList.innerHTML = "No action items detected.";
    } else {

        actionsList.innerHTML = actions.map(action => `
            <div class="item">
                <p>
                    ${escapeHTML(action.task)}
                </p>
                <div class="meta">
                    <span class="tag">
                        Owner: ${escapeHTML(action.owner)}
                    </span>
                    <span class="tag">
                        Deadline: ${escapeHTML(action.deadline)}
                    </span>

                    <span class="tag status">
                        ${escapeHTML(action.status)}
                    </span>
                </div>
            </div>
        `).join("");
    }

    // RISKS
    const risksList = document.getElementById("risksList");
    const risks = data.risks || [];
    risksList.classList.remove("empty");
    if (!risks.length) {
        risksList.innerHTML = "No risks detected.";
    } else {
        risksList.innerHTML = risks.map(risk => {
            const level = String(
                risk.level || "Medium"
            ).toLowerCase();
            return `
                <div class="item risk-${level}">
                    <p>
                        <b>
                            ${escapeHTML(risk.title)}
                        </b>
                    </p>

                    <div class="muted">
                        ${escapeHTML(risk.detail)}
                    </div>

                    <div class="meta">

                        <span class="tag">
                            ${escapeHTML(risk.level)}
                            Priority
                        </span>
                    </div>
                </div>
            `;
        }).join("");
    }


    // DEPENDENCY MAP
    renderDependencyMap(
        data.dependencies || []
    );

    if (window.lucide) {
        lucide.createIcons();
    }
}


// DEPENDENCY MAP
function renderDependencyMap(dependencies) {
    const dependencyMap = document.getElementById(
        "dependencyMap"
    );

    dependencyMap.classList.remove("empty");
    if (!dependencies.length) {
        dependencyMap.innerHTML =
            "No dependencies detected yet.";
        dependencyMap.classList.add("empty");
        return;
    }

    // Create connected dependency chains
    const chains = buildDependencyChains(dependencies);
    dependencyMap.innerHTML = chains.map(chain => {
        return chain.map((node, index) => {
            const nodeHTML = `
                <div class="dependency-node">
                    ${escapeHTML(node)}
                </div>
            `;

            if (index === chain.length - 1) {
                return nodeHTML;
            }

            const dependency = dependencies.find(dep =>
                dep.from === node &&
                dep.to === chain[index + 1]
            );

            return nodeHTML + `
                <div class="dependency-arrow">

                    →

                    <small>
                        ${escapeHTML(
                            dependency
                                ? dependency.type
                                : "Required Before"
                        )}
                    </small>
                </div>
            `;
        }).join("");
    }).join("");
}

// BUILD DEPENDENCY CHAINS
function buildDependencyChains(dependencies) {
    const outgoing = new Map();
    const incoming = new Set();
    dependencies.forEach(dep => {
        if (!outgoing.has(dep.from)) {
            outgoing.set(dep.from, []);
        }
        outgoing.get(dep.from).push(dep.to);
        incoming.add(dep.to);
    });

    const roots = dependencies
        .map(dep => dep.from)
        .filter(node => !incoming.has(node))
        .filter((node, index, arr) =>
            arr.indexOf(node) === index
        );

    const chains = [];
    const visited = new Set();
    function walk(node, chain) {
        if (chain.includes(node)) {
            return;
        }

        const nextChain = [...chain, node];
        const nextNodes = outgoing.get(node) || [];
        if (!nextNodes.length) {
            chains.push(nextChain);
            return;
        }

        nextNodes.forEach(next => {
            walk(next, nextChain);
        });
    }

    roots.forEach(root => {
        walk(root, []);
        visited.add(root);
    });

    // Handle disconnected relationships
    dependencies.forEach(dep => {
        if (!visited.has(dep.from)) {
            walk(dep.from, []);
            visited.add(dep.from);
        }

    });

    return chains.length ? chains : [
        [dependencies[0].from, dependencies[0].to]
    ];
}

// HTML ESCAPE
function escapeHTML(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}