import discord
from discord.ext import commands
import numpy as np

# Administration commands can only be used by members with this role.
admin_role: str = "PokeBotAdmin"

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates the minimum edit distance between s1 and s2.
    The minimum edit distance is the least number of character deletions, insertions
    and substitutions applied to s1 in order to get s2.

    Args:
        s1 (str): The first string.
        s2 (str): The target string.

    Returns:
        int: The minimum edit distance between s1 and s2.
    """

    # Fill matrix with dimension (len(s1) + 1) x (len(s2) + 1)
    l1 = (len(s1) + 1)
    l2 = (len(s2) + 1)
    dp = np.zeros((l1, l2))

    # Initialize first row and column (distance between prefix and the empty string)
    for t1 in range(0, l1):
        dp[t1][0] = t1
    
    for t2 in range(0, l2):
        dp[0][t2] = t2

    # Now iterate through every cell of the matrix, representing the distance between prefixes.
    
    for t1 in range(1, l1):
        for t2 in range(1, l2):
            # If both characters are equal, then the distance between prefixes is the same
            # as the distance between the previous prefixes.
            if s1[t1 - 1] == s2[t2 - 1]:
                dp[t1][t2] = dp[t1 - 1][t2 - 1]
            # Otherwise, it means that we must edit the string, so calculate the minimum
            # between the distance after deleting, adding and substituting characters from the string
            # and adding one to the edit distance.
            else:
                dp[t1][t2] = min(dp[t1 - 1][t2 - 1], dp[t1][t2 - 1], dp[t1 - 1][t2]) + 1

    # The minimum edit distance will be the value in the right lower corner of the matrix.
    return dp[l1 - 1][l2 - 1]

    
# Operations for getting information about members based on context
class MemberCast(commands.MemberConverter):

    # Get user display name based on user id
    async def get_display_name(self, ctx, id):
        member = await super().convert(ctx, id)
        return member.display_name

