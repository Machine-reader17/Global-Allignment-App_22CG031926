from alignment import AlignmentTool

def test_global():
    tool = AlignmentTool()
    # GATTA vs GCAT
    # Match: 2, Mismatch: -1, Gap: -2
    # G A T T A
    # G C A - T
    # G-G: 2
    # A-C: -1
    # T-A: -1
    # T--: -2
    # A-T: -1
    # Total: 2 - 1 - 1 - 2 - 1 = -3? 
    # Let's see what the algorithm says.
    
    result = tool.global_alignment("GATTA", "GCAT", 2, -1, -2)
    print(f"Global Alignment Score: {result['score']}")
    print(f"Align 1: {result['align1']}")
    print(f"Align 2: {result['align2']}")
    # Expected score for GATTA vs GCAT with these params:
    # Matrix:
    #       -   G   A   T   T   A
    # -     0  -2  -4  -6  -8 -10
    # G    -2   2   0  -2  -4  -6
    # C    -4   0   1  -1  -3  -5
    # A    -6  -2   2   0  -2  -1
    # T    -8  -4   0   4   2   0
    # Final score: 0
    
def test_local():
    tool = AlignmentTool()
    result = tool.local_alignment("GATTA", "GCAT", 2, -1, -2)
    print(f"Local Alignment Score: {result['score']}")
    print(f"Align 1: {result['align1']}")
    print(f"Align 2: {result['align2']}")
    # Local should find AT vs AT or something similar.
    # Score for AT vs AT: 2+2 = 4.

if __name__ == "__main__":
    print("Testing Global Alignment...")
    test_global()
    print("\nTesting Local Alignment...")
    test_local()
