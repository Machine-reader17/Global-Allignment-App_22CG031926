document.addEventListener('DOMContentLoaded', () => {
    const alignBtn = document.getElementById('alignBtn');
    const resetBtn = document.getElementById('resetBtn');
    const resultsSection = document.getElementById('resultsSection');
    const errorBox = document.getElementById('errorBox');
    const errorMessage = document.getElementById('errorMessage');

    // Alignment Result Elements
    const finalScore = document.getElementById('finalScore');
    const alignString1 = document.getElementById('alignString1');
    const alignmentMatch = document.getElementById('alignmentMatch');
    const alignString2 = document.getElementById('alignString2');
    const matrixContainer = document.getElementById('matrixContainer');

    alignBtn.addEventListener('click', async () => {
        // Clear previous state
        errorBox.style.display = 'none';
        resultsSection.style.display = 'none';
        alignBtn.disabled = true;
        alignBtn.textContent = 'Aligning...';

        const data = {
            seq1: document.getElementById('seq1').value,
            seq2: document.getElementById('seq2').value,
            match: document.getElementById('match').value,
            mismatch: document.getElementById('mismatch').value,
            gap: document.getElementById('gap').value,
            type: document.querySelector('input[name="alignType"]:checked').value
        };

        try {
            const response = await fetch('/api/align', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                displayResults(result);
            } else {
                showError(result.error || 'An error occurred during alignment.');
            }
        } catch (error) {
            showError('Could not connect to the server. Make sure the backend is running.');
            console.error(error);
        } finally {
            alignBtn.disabled = false;
            alignBtn.textContent = 'Run Alignment';
        }
    });

    resetBtn.addEventListener('click', () => {
        document.getElementById('seq1').value = '';
        document.getElementById('seq2').value = '';
        resultsSection.style.display = 'none';
        errorBox.style.display = 'none';
    });

    function displayResults(data) {
        finalScore.textContent = data.score;
        alignString1.textContent = data.align1;
        alignString2.textContent = data.align2;

        // Generate match indicators
        let indicators = '';
        for (let i = 0; i < data.align1.length; i++) {
            if (data.align1[i] === data.align2[i] && data.align1[i] !== '-') {
                indicators += '|';
            } else {
                indicators += ' ';
            }
        }
        alignmentMatch.textContent = indicators;

        renderMatrix(data);
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function renderMatrix(data) {
        const matrix = data.matrix;
        const seq1 = data.seq1_orig;
        const seq2 = data.seq2_orig;
        const path = data.path; // Array of [i, j]

        const rows = matrix.length;
        const cols = matrix[0].length;

        // Create CSS Grid layout
        // cols+2 for: blank corner, seq1 chars, blank
        // rows+2 for: blank corner, seq2 chars, blank
        matrixContainer.style.gridTemplateColumns = `repeat(${cols + 2}, 50px)`;
        matrixContainer.innerHTML = '';

        // Helper to check if [i, j] is in path
        const isInPath = (r, c) => path.some(p => p[0] === r && p[1] === c);

        // Row 0: Headers (Sequence 1)
        // [Corner] [Gap] [S1[0]] [S1[1]] ...
        matrixContainer.appendChild(createCell('', 'header')); // Top-left corner
        matrixContainer.appendChild(createCell('-', 'header')); // Gap indicator
        for (let j = 0; j < seq1.length; j++) {
            matrixContainer.appendChild(createCell(seq1[j], 'header'));
        }

        // Subsequent Rows
        for (let i = 0; i < rows; i++) {
            // Row Header (Sequence 2 char or Gap)
            if (i === 0) {
                matrixContainer.appendChild(createCell('-', 'header'));
            } else {
                matrixContainer.appendChild(createCell(seq2[i - 1], 'header'));
            }

            // Matrix Values
            for (let j = 0; j < cols; j++) {
                const cellClass = isInPath(i, j) ? 'path' : '';
                matrixContainer.appendChild(createCell(matrix[i][j], cellClass));
            }
        }
    }

    function createCell(content, className = '') {
        const cell = document.createElement('div');
        cell.className = `matrix-cell ${className}`;
        cell.textContent = content;
        return cell;
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorBox.style.display = 'block';
    }
});
