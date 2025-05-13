// Carrega o Pyodide e inicializa o ambiente Python
async function loadPyodideAndPackages() {
    const pyodide = await loadPyodide();
    try {
        // Carregando pacotes essenciais
        await pyodide.loadPackage(['micropip', 'scipy']);
        await pyodide.runPythonAsync(`
            import micropip
            await micropip.install('numpy')
            await micropip.install('networkx')
            await micropip.install('scikit-fuzzy')
        `);
    } catch (error) {
        throw new Error('Erro ao carregar os pacotes: ' + error.message);
    }
    return pyodide;
}

// Carrega o código Python de fuzzy.py
async function loadPythonCode() {
    try {
        const response = await fetch('fuzzy.py');
        if (!response.ok) {
            throw new Error(`Falha ao carregar fuzzy.py: ${response.status} ${response.statusText}`);
        }
        return await response.text();
    } catch (error) {
        throw new Error(`Erro ao buscar fuzzy.py: ${error.message}. Certifique-se de que o arquivo está na mesma pasta que index.html e que o servidor local está rodando.`);
    }
}

// Carrega o código Python de rules.py
async function loadRulesCode() {
    try {
        const response = await fetch('rules.py');
        if (!response.ok) {
            throw new Error(`Falha ao carregar rules.py: ${response.status} ${response.statusText}`);
        }
        return await response.text();
    } catch (error) {
        throw new Error(`Erro ao buscar rules.py: ${error.message}. Certifique-se de que o arquivo está na mesma pasta que index.html`);
    }
}

// Inicializa o Pyodide e carrega o código Python
let pyodide;
let pyodideReady = false;
(async () => {
    try {
        pyodide = await loadPyodideAndPackages();

        // Carregando rules.py antes do fuzzy.py
        const rulesCode = await loadRulesCode();
        await pyodide.runPythonAsync(rulesCode);

        const pythonCode = await loadPythonCode();
        await pyodide.runPythonAsync(pythonCode);

        pyodideReady = true;
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('calculate-btn').disabled = false;

        // Cria os segmentos dinamicamente
        const segmentsContainer = document.getElementById('segments');
        for (let i = 1; i <= 4; i++) {
            segmentsContainer.innerHTML += `
                <div class="segment border p-4 rounded">
                    <h3 class="text-lg font-medium mb-2">Segmento ${i}</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium">Densidade (0-200 carros)</label>
                            <input type="number" name="density-${i}" min="0" max="200" value="100" class="w-full p-2 border rounded" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium">Velocidade (0-70 km/h)</label>
                            <input type="number" name="velocity-${i}" min="0" max="70" value="40" class="w-full p-2 border rounded" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium">Tempo de Espera (0-150 s)</label>
                            <input type="number" name="wait-${i}" min="0" max="150" value="60" class="w-full p-2 border rounded" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium">Incidentes (0-6)</label>
                            <input type="number" name="incidents-${i}" min="0" max="6" step="0.1" value="2" class="w-full p-2 border rounded" required>
                        </div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('error').classList.remove('hidden');
        document.getElementById('error').textContent = 'Erro ao inicializar o sistema: ' + error.message;
    }
})();

// Manipula o envio do formulário
document.getElementById('traffic-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!pyodideReady) {
        document.getElementById('error').classList.remove('hidden');
        document.getElementById('error').textContent = 'Sistema ainda não inicializado. Por favor, aguarde.';
        return;
    }

    const formData = new FormData(e.target);
    const inputs = [];
    for (let i = 1; i <= 4; i++) {
        const density = parseFloat(formData.get(`density-${i}`));
        const velocity = parseFloat(formData.get(`velocity-${i}`));
        const wait = parseFloat(formData.get(`wait-${i}`));
        const incidents = parseFloat(formData.get(`incidents-${i}`));
        inputs.push([density, velocity, wait, incidents]);
    }

    try {
        // Executa o código Python
        const result = await pyodide.runPythonAsync(`import json\njson.dumps(compute_green_times(${JSON.stringify(inputs)}))`);
        const parsedResult = JSON.parse(result);
        const greenTimes = parsedResult[0];
        const memberships = parsedResult[1];

        // Limpa gráficos antigos
        const graphsContainer = document.getElementById('graphs-container');
        graphsContainer.innerHTML = '';

        // Exibe os tempos de verde
        const resultsTable = document.getElementById('results-table');
        resultsTable.innerHTML = '';
        greenTimes.forEach((time, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="border p-2">Semáforo ${index + 1}</td>
                <td class="border p-2">${time.toFixed(2)} segundos</td>
            `;
            resultsTable.appendChild(row);
        });
        document.getElementById('results').classList.remove('hidden');

        // Exibe os gráficos de resultado final
        memberships.forEach((membership, index) => {
            const canvasId = `segment-final-chart-${index + 1}`;
            graphsContainer.innerHTML += `<canvas id="${canvasId}" width="800" height="400" class="mb-4"></canvas>`;
            const ctx = document.getElementById(canvasId).getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: membership.green_time.range,
                    datasets: [
                        { label: 'Curto', data: membership.green_time.curto, borderColor: 'blue', fill: false },
                        { label: 'Médio', data: membership.green_time.medio, borderColor: 'orange', fill: false },
                        { label: 'Longo', data: membership.green_time.longo, borderColor: 'green', fill: false }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: `Resultado Final - Segmento ${index + 1}`
                        }
                    }
                }
            });
        });
        document.getElementById('graphs').classList.remove('hidden');

        // Oculta mensagem de erro
        document.getElementById('error').classList.add('hidden');
    } catch (error) {
        document.getElementById('error').classList.remove('hidden');
        document.getElementById('error').textContent = 'Erro ao calcular tempos de verde: ' + error.message;
    }
});
