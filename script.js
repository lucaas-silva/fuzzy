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

// Inicializa o Pyodide e carrega o código Python
let pyodide;
let pyodideReady = false;
(async () => {
    try {
        pyodide = await loadPyodideAndPackages();
        const pythonCode = await loadPythonCode();
        await pyodide.runPythonAsync(pythonCode);
        pyodideReady = true;
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('calculate-btn').disabled = false;
        
        // Cria os segmentos dinamicamente
        const segmentsContainer = document.getElementById('segments');
        for (let i = 1; i <= 4; i++) {
            segmentsContainer.innerHTML += `
                <div class="segment">
                    <h3 class="text-lg font-medium mb-2">🚥 Segmento ${i}</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium">🚗 Densidade (0-200 carros)</label>
                            <input type="number" name="density-${i}" min="0" max="200" value="100" class="w-full p-2 border rounded" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium">🏎️ Velocidade (0-70 km/h)</label>
                            <input type="number" name="velocity-${i}" min="0" max="70" value="40" class="w-full p-2 border rounded" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium">⏱️ Tempo de Espera (0-150 s)</label>
                            <input type="number" name="wait-${i}" min="0" max="150" value="60" class="w-full p-2 border rounded" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium">🚨 Incidentes (0-6)</label>
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
function displayResults(greenTimes) {
    const resultsTable = document.getElementById('results-table');
    resultsTable.innerHTML = '';
    greenTimes.forEach((time, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="border p-3">🚥 Semáforo ${index + 1}</td>
            <td class="border p-3">⏱️ ${time.toFixed(2)} segundos</td>
        `;
        resultsTable.appendChild(row);
    });
    document.getElementById('results').classList.remove('hidden');
}

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
        const result = await pyodide.runPythonAsync(`import json\njson.dumps(compute_green_times(${JSON.stringify(inputs)}))`);
        const parsedResult = JSON.parse(result);
        console.log('Tempos de verde:', parsedResult[0]);
        console.log('Ajustes aplicados:', parsedResult[2]); // Adicionado para depurar os ajustes
        console.log('Pertinências e valores:', parsedResult[1]);
        displayResults(parsedResult[0]);
        document.getElementById('error').classList.add('hidden');
    } catch (error) {
        document.getElementById('error').classList.remove('hidden');
        document.getElementById('error').textContent = 'Erro ao calcular tempos de verde: ' + error.message;
    }
});
