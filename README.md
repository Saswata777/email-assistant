<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Email Assistant (Inbox-IQ) Showcase</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- 
        Chosen Palette: Cool Indigo & Slate
        Application Structure Plan: The SPA is designed as a single-page, top-down narrative showcase. This structure was chosen to guide a user (like a recruiter or collaborator) through the project's story in a logical flow: what it is, the problem it solves, how it works, what it's built with, and how to use it. Key interactions include a clickable workflow diagram to explain the system's logic step-by-step and a dynamic chart in a dashboard mockup to demonstrate the project's data-handling capabilities. This is more engaging and digestible than a static text document.
        Visualization & Content Choices: 
        - Project Workflow: Report Info -> System Process Flow -> Goal: Organize/Explain -> Viz: Interactive Diagram (HTML/CSS/JS) -> Interaction: Click nodes to reveal detailed explanations -> Justification: Breaks down a complex system into understandable, user-explorable steps.
        - Dashboard Mockup: Report Info -> Key Features (Analytics) -> Goal: Inform/Compare -> Viz: Bar Chart (Chart.js) -> Interaction: Filter buttons update chart data -> Justification: Visually demonstrates the end-product's analytical power and provides a tangible look at the UI.
        - Tech Stack: Report Info -> Technologies Used -> Goal: Inform -> Viz: Icon-based Grid (HTML/Tailwind) -> Interaction: Subtle hover effects -> Justification: A quick, scannable, and visually appealing way to present the technologies.
        CONFIRMATION: NO SVG graphics used. NO Mermaid JS used.
    -->
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc; /* slate-50 */
            color: #1e293b; /* slate-800 */
        }
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            height: 300px;
            max-height: 400px;
        }
        @media (min-width: 640px) {
            .chart-container {
                height: 350px;
            }
        }
        .gradient-text {
            background: linear-gradient(to right, #4f46e5, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .step-connector {
            flex-grow: 1;
            height: 2px;
            background-color: #cbd5e1; /* slate-300 */
        }
        .step.active {
            border-color: #4f46e5; /* indigo-600 */
            color: #4f46e5;
            transform: scale(1.05);
        }
    </style>
</head>
<body class="antialiased">

    <header class="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-200">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <span class="text-2xl">🤖</span>
                    <h1 class="text-xl font-bold text-slate-800">Inbox-IQ Showcase</h1>
                </div>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="#features" class="text-slate-600 hover:text-indigo-600 font-medium">Features</a>
                    <a href="#workflow" class="text-slate-600 hover:text-indigo-600 font-medium">Workflow</a>
                    <a href="#stack" class="text-slate-600 hover:text-indigo-600 font-medium">Tech Stack</a>
                    <a href="#setup" class="text-slate-600 hover:text-indigo-600 font-medium">Setup</a>
                    <a href="https://github.com/Saswata777/email-assistant" target="_blank" rel="noopener noreferrer" class="text-slate-600 hover:text-indigo-600 font-medium">GitHub</a>
                </div>
            </div>
        </nav>
    </header>

    <main>
        <section id="hero" class="py-20 sm:py-24 lg:py-32 text-center bg-white">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                <h2 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight">
                    AI-Powered <span class="gradient-text">Email Assistant</span>
                </h2>
                <p class="mt-6 text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto">
                    An intelligent solution to automate and streamline support email management. It uses NLP to categorize, prioritize, and generate responses, all on a clean, intuitive dashboard.
                </p>
                <div class="mt-10 flex flex-col sm:flex-row justify-center items-center gap-4">
                    <a href="#workflow" class="bg-indigo-600 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:bg-indigo-700 transition-colors w-full sm:w-auto">See How It Works</a>
                    <a href="https://github.com/Saswata777/email-assistant" target="_blank" rel="noopener noreferrer" class="bg-white text-indigo-600 font-semibold px-6 py-3 rounded-lg shadow-md border border-indigo-200 hover:bg-indigo-50 transition-colors w-full sm:w-auto">View on GitHub</a>
                </div>
            </div>
        </section>

        <section id="features" class="py-16 sm:py-20 bg-slate-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center">
                    <h3 class="text-3xl font-bold tracking-tight">Project Features & Dashboard</h3>
                    <p class="mt-4 text-lg text-slate-600">A centralized dashboard provides at-a-glance analytics and full control over the automated workflow.</p>
                </div>

                <div class="mt-12 grid lg:grid-cols-5 gap-8 items-center">
                    <div class="lg:col-span-2 space-y-6">
                        <div class="p-4 bg-white rounded-lg shadow-sm">
                            <h4 class="font-semibold">📧 Automated Email Filtering</h4>
                            <p class="text-sm text-slate-500">Fetches and filters support emails via the Gmail API.</p>
                        </div>
                        <div class="p-4 bg-white rounded-lg shadow-sm">
                            <h4 class="font-semibold">🧠 AI-Powered Triage</h4>
                            <p class="text-sm text-slate-500">Uses an LLM for sentiment and urgency detection.</p>
                        </div>
                        <div class="p-4 bg-white rounded-lg shadow-sm">
                            <h4 class="font-semibold">✍️ Intelligent Auto-Responses</h4>
                            <p class="text-sm text-slate-500">Generates context-aware replies using a RAG pipeline.</p>
                        </div>
                         <div class="p-4 bg-white rounded-lg shadow-sm">
                            <h4 class="font-semibold">⏰ Scheduled Fetching</h4>
                            <p class="text-sm text-slate-500">Periodically checks for new emails with a background scheduler.</p>
                        </div>
                    </div>
                    <div class="lg:col-span-3 bg-white p-6 rounded-xl shadow-lg">
                        <div class="flex justify-between items-center mb-4">
                            <h4 class="text-lg font-semibold">Inbox Analytics</h4>
                            <div id="chart-filters" class="flex space-x-2">
                                <button data-period="24h" class="filter-btn bg-indigo-500 text-white px-3 py-1 text-sm rounded-md">24h</button>
                                <button data-period="7d" class="filter-btn bg-slate-200 text-slate-700 px-3 py-1 text-sm rounded-md">7d</button>
                                <button data-period="30d" class="filter-btn bg-slate-200 text-slate-700 px-3 py-1 text-sm rounded-md">30d</button>
                            </div>
                        </div>
                        <div class="chart-container">
                            <canvas id="emailChart"></canvas>
                        </div>
                        <p class="text-xs text-center text-slate-500 mt-2">Interact with the filters to see how the dashboard dynamically displays email data based on urgency.</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="workflow" class="py-16 sm:py-20 bg-white">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center">
                    <h3 class="text-3xl font-bold tracking-tight">System Workflow</h3>
                    <p class="mt-4 text-lg text-slate-600">Follow the journey of an email from arrival to response. Click on each step to learn more.</p>
                </div>

                <div class="mt-12">
                    <div class="flex items-center justify-center">
                        <div class="flex items-center w-full max-w-4xl">
                            <button class="step" data-step="1">Fetch</button>
                            <div class="step-connector"></div>
                            <button class="step" data-step="2">Process</button>
                            <div class="step-connector"></div>
                            <button class="step" data-step="3">Analyze</button>
                            <div class="step-connector"></div>
                            <button class="step" data-step="4">Respond</button>
                            <div class="step-connector"></div>
                            <button class="step" data-step="5">Display</button>
                        </div>
                    </div>
                    <div id="workflow-details" class="mt-8 min-h-[100px] bg-slate-50 p-6 rounded-lg shadow-inner text-center max-w-3xl mx-auto">
                        <p class="text-slate-600">Select a step above to see its description.</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="stack" class="py-16 sm:py-20 bg-slate-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center">
                    <h3 class="text-3xl font-bold tracking-tight">Technology Stack</h3>
                    <p class="mt-4 text-lg text-slate-600">The tools and technologies that power the AI Email Assistant.</p>
                </div>
                <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="bg-white p-6 rounded-lg shadow-sm">
                        <h4 class="text-xl font-semibold mb-4 text-center">Backend</h4>
                        <div class="grid grid-cols-2 gap-4 text-center">
                            <div class="p-2">🐍 Python</div><div class="p-2">🌐 Flask</div>
                            <div class="p-2">💎 Gemini API</div><div class="p-2">📧 Gmail API</div>
                            <div class="p-2">💾 SQLite</div><div class="p-2">🕒 APScheduler</div>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-sm">
                        <h4 class="text-xl font-semibold mb-4 text-center">Frontend</h4>
                        <div class="grid grid-cols-2 gap-4 text-center">
                             <div class="p-2">⚛️ Next.js</div><div class="p-2">📘 React</div>
                             <div class="p-2">💨 Tailwind CSS</div><div class="p-2">📈 Chart.js</div>
                        </div>
                    </div>
                     <div class="bg-white p-6 rounded-lg shadow-sm">
                        <h4 class="text-xl font-semibold mb-4 text-center">Core Concepts</h4>
                        <div class="grid grid-cols-2 gap-4 text-center">
                            <div class="p-2">🗣️ NLP</div><div class="p-2">📚 RAG</div>
                            <div class="p-2">🔗 REST APIs</div><div class="p-2">🤖 AI/ML</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="setup" class="py-16 sm:py-20 bg-white">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center">
                    <h3 class="text-3xl font-bold tracking-tight">Getting Started</h3>
                    <p class="mt-4 text-lg text-slate-600">Follow these steps to set up and run the project locally.</p>
                </div>
                <div class="mt-12 space-y-8">
                    <div>
                        <h4 class="font-semibold text-lg mb-2">1. Clone the Repository</h4>
                        <pre class="bg-slate-800 text-slate-200 p-4 rounded-lg text-sm overflow-x-auto"><code>git clone https://github.com/your-username/Email-Assistant.git
cd Email-Assistant</code></pre>
                    </div>
                     <div>
                        <h4 class="font-semibold text-lg mb-2">2. Backend Setup</h4>
                        <pre class="bg-slate-800 text-slate-200 p-4 rounded-lg text-sm overflow-x-auto"><code>cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set up your .env file and credentials.json</code></pre>
                    </div>
                     <div>
                        <h4 class="font-semibold text-lg mb-2">3. Frontend Setup</h4>
                        <pre class="bg-slate-800 text-slate-200 p-4 rounded-lg text-sm overflow-x-auto"><code>cd ../inbox-iq
npm install
# Set up frontend environment variables if any</code></pre>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    <footer class="bg-slate-800 text-white py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-slate-400">
            <p>&copy; 2025 AI-Powered Email Assistant. A project showcase.</p>
        </div>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const chartData = {
                '24h': [12, 5, 2],
                '7d': [85, 42, 15],
                '30d': [350, 180, 65]
            };
            const labels = ['Not Urgent', 'Normal', 'Urgent'];
            const ctx = document.getElementById('emailChart').getContext('2d');
            const emailChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Emails Processed',
                        data: chartData['24h'],
                        backgroundColor: ['#60a5fa', '#a78bfa', '#f87171'],
                        borderColor: ['#3b82f6', '#8b5cf6', '#ef4444'],
                        borderWidth: 1,
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    scales: {
                        x: { beginAtZero: true, grid: { display: false } },
                        y: { grid: { display: false } }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return ` ${context.dataset.label}: ${context.raw}`;
                                }
                            }
                        }
                    }
                }
            });

            const filterButtons = document.querySelectorAll('.filter-btn');
            filterButtons.forEach(button => {
                button.addEventListener('click', () => {
                    filterButtons.forEach(btn => {
                        btn.classList.remove('bg-indigo-500', 'text-white');
                        btn.classList.add('bg-slate-200', 'text-slate-700');
                    });
                    button.classList.add('bg-indigo-500', 'text-white');
                    button.classList.remove('bg-slate-200', 'text-slate-700');
                    
                    const period = button.dataset.period;
                    emailChart.data.datasets[0].data = chartData[period];
                    emailChart.update();
                });
            });

            const steps = document.querySelectorAll('.step');
            const detailsContainer = document.getElementById('workflow-details');
            const stepDetails = {
                1: {
                    title: 'Step 1: Fetch Emails',
                    description: 'The system securely connects to a specified email account using the Gmail API. A background scheduler runs periodically to fetch all new, unread emails.'
                },
                2: {
                    title: 'Step 2: Process & Filter',
                    description: 'Each incoming email is processed. The system filters for emails whose subject lines contain keywords like "Support", "Query", or "Help" to identify relevant messages.'
                },
                3: {
                    title: 'Step 3: AI Analysis & Triage',
                    description: 'Relevant emails are sent to the Gemini LLM for deep analysis. The model performs sentiment analysis (Positive/Negative/Neutral) and detects urgency based on keywords, then categorizes and prioritizes the email.'
                },
                4: {
                    title: 'Step 4: Generate Intelligent Response',
                    description: 'Using a Retrieval-Augmented Generation (RAG) pipeline, the system generates a context-aware draft reply. It pulls relevant information from a knowledge base to answer questions professionally and empathetically.'
                },
                5: {
                    title: 'Step 5: Display on Dashboard',
                    description: 'The original email, its priority, sentiment, extracted information, and the AI-generated draft reply are all presented on the user-friendly Next.js dashboard for final review and action.'
                }
            };

            steps.forEach(step => {
                step.addEventListener('click', () => {
                    steps.forEach(s => s.classList.remove('active'));
                    step.classList.add('active');
                    const stepKey = step.dataset.step;
                    const detail = stepDetails[stepKey];
                    detailsContainer.innerHTML = `<h4 class="font-bold text-lg text-slate-800">${detail.title}</h4><p class="mt-2 text-slate-600">${detail.description}</p>`;
                });
            });

            // Set initial active step for workflow
            steps[0].click();
            
            // CSS for step buttons
            const style = document.createElement('style');
            style.textContent = `
                .step {
                    flex-shrink: 0;
                    width: 80px;
                    height: 80px;
                    border-radius: 9999px;
                    border: 2px solid #cbd5e1; /* slate-300 */
                    background-color: #ffffff;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                    color: #475569; /* slate-600 */
                    transition: all 0.2s ease-in-out;
                    cursor: pointer;
                }
                .step:hover {
                    border-color: #a5b4fc; /* indigo-300 */
                    color: #3730a3; /* indigo-800 */
                }
            `;
            document.head.append(style);
        });
    </script>
</body>
</html>


