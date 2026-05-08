class AlignmentTool:
    @staticmethod
    def global_alignment(seq1, seq2, match_score, mismatch_score, gap_penalty):
        """Needleman-Wunsch Algorithm for Global Alignment"""
        n, m = len(seq1), len(seq2)
        # Initialize matrix
        matrix = [[0] * (m + 1) for _ in range(n + 1)]
        
        # Fill first row and column with gap penalties
        for i in range(1, n + 1):
            matrix[i][0] = i * gap_penalty
        for j in range(1, m + 1):
            matrix[0][j] = j * gap_penalty
            
        # Fill the rest of the matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                score = match_score if seq1[i-1] == seq2[j-1] else mismatch_score
                matrix[i][j] = max(
                    matrix[i-1][j-1] + score,      # Match/Mismatch
                    matrix[i-1][j] + gap_penalty,   # Deletion
                    matrix[i][j-1] + gap_penalty    # Insertion
                )
        
        # Traceback
        align1, align2 = "", ""
        i, j = n, m
        path = [(i, j)]
        
        while i > 0 or j > 0:
            current_score = matrix[i][j]
            
            if i > 0 and j > 0:
                score = match_score if seq1[i-1] == seq2[j-1] else mismatch_score
                if current_score == matrix[i-1][j-1] + score:
                    align1 = seq1[i-1] + align1
                    align2 = seq2[j-1] + align2
                    i -= 1
                    j -= 1
                    path.append((i, j))
                    continue
            
            if i > 0 and current_score == matrix[i-1][j] + gap_penalty:
                align1 = seq1[i-1] + align1
                align2 = "-" + align2
                i -= 1
                path.append((i, j))
            else:
                align1 = "-" + align1
                align2 = seq2[j-1] + align2
                j -= 1
                path.append((i, j))
                
        return {
            'type': 'global',
            'score': matrix[n][m],
            'matrix': matrix,
            'align1': align1,
            'align2': align2,
            'path': path[::-1] # Return path from start to end
        }

    @staticmethod
    def local_alignment(seq1, seq2, match_score, mismatch_score, gap_penalty):
        """Smith-Waterman Algorithm for Local Alignment"""
        n, m = len(seq1), len(seq2)
        # Initialize matrix with 0s
        matrix = [[0] * (m + 1) for _ in range(n + 1)]
        
        max_score = -1
        max_pos = (0, 0)
        
        # Fill matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                score = match_score if seq1[i-1] == seq2[j-1] else mismatch_score
                matrix[i][j] = max(
                    0,
                    matrix[i-1][j-1] + score,
                    matrix[i-1][j] + gap_penalty,
                    matrix[i][j-1] + gap_penalty
                )
                
                if matrix[i][j] >= max_score:
                    max_score = matrix[i][j]
                    max_pos = (i, j)
        
        # Traceback from max_pos
        align1, align2 = "", ""
        i, j = max_pos
        path = [(i, j)]
        
        while i > 0 and j > 0 and matrix[i][j] > 0:
            current_score = matrix[i][j]
            score = match_score if seq1[i-1] == seq2[j-1] else mismatch_score
            
            if current_score == matrix[i-1][j-1] + score:
                align1 = seq1[i-1] + align1
                align2 = seq2[j-1] + align2
                i -= 1
                j -= 1
            elif current_score == matrix[i-1][j] + gap_penalty:
                align1 = seq1[i-1] + align1
                align2 = "-" + align2
                i -= 1
            else:
                align1 = "-" + align1
                align2 = seq2[j-1] + align2
                j -= 1
            
            path.append((i, j))
            
        return {
            'type': 'local',
            'score': max_score,
            'matrix': matrix,
            'align1': align1,
            'align2': align2,
            'path': path[::-1]
        }
