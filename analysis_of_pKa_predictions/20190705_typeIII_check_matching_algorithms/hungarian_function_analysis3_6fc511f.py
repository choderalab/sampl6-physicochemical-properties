def hungarian_matching(pred_pKas, exp_pKa_means, exp_pKa_SEMs, exp_pKa_IDs):
    """Perform Hungarian algorithm matching of pKa values.
    Original source by Kiril Lanevskij (ACD Labs).
    Args:
        predicted : array of predicted pKas
        experimental: array of experimental pKas
    """

    matched = pd.DataFrame()
    cost = []
    predicted = pred_pKas
    experimental = exp_pKa_means

    # Our cost matrix will have the same size as no. of exp. or pred. pKa values, whichever is larger
    sz = max(len(experimental), len(predicted))
    for i in range(sz):
        cost.append([])
        for j in range(sz):
            # Calculate mapping cost as an absolute diff. between exp. and pred. pKa values
            if i < len(experimental) and j < len(predicted):
                # Cost is defined as squared error
                cost_se = (predicted[j]-experimental[i])**2
                cost[i].append(cost_se)
            # Assign zero cost if we are out of bounds
            else:
                cost[i].append(0)
    # Perform mapping itself, row_indices => exp. data, col_indices => pred. pKa
    row_indices, col_indices = scipy.optimize.linear_sum_assignment(cost)
    for i, row_id in enumerate(row_indices):
        col_id = col_indices[i]
        # Ignore the entry if we are out of bounds
        if row_id >= len(experimental) or col_id >= len(predicted): continue
        # Otherwise assign a match
        match = {"pred pKa" : predicted[col_id], 'pKa mean': predicted[col_id], 'pKa SEM': exp_pKa_SEMs[row_id], 'pKa ID': exp_pKa_IDs[row_id]}
        matched = matched.append(match, ignore_index=True)

    return matched

