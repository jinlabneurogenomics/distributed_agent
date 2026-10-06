"""Tabulate grounded stories and saved survey comparator reports."""
import json
from pathlib import Path
import pandas as pd
from .paths import RUNS, INPUTS
from .common import write_table


def prepare():
    story_dir = RUNS / 'survey/distributed_agents'
    ranking = pd.DataFrame(json.loads((story_dir / 'adjudicated_ranking.json').read_text())['ranked'])
    stories = []
    for path in sorted((story_dir / 'grounded_stories').glob('*.json')):
        row = json.loads(path.read_text())
        stories.append({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
                        for key, value in row.items()})
    frame = pd.DataFrame(stories)
    if len(frame) != 144 or frame.story_id.duplicated().any() or set(frame.story_id) != set(ranking.story_id):
        raise ValueError('Expected 144 uniquely identified and ranked stories')
    for column in ranking:
        if ranking[column].map(lambda x: isinstance(x, (list, dict))).any():
            ranking[column] = ranking[column].map(lambda x: json.dumps(x, ensure_ascii=False))
    write_table(frame.merge(ranking, on='story_id', validate='one_to_one').sort_values('rank'), 'survey/grounded_stories.csv')
    reports = sorted((RUNS / 'survey/codex').glob('r*/report.md'))
    if len(reports) != 3:
        raise ValueError('Expected three Codex30-caveat survey comparator reports')
    write_table(pd.DataFrame([dict(method='codex30-caveat', replicate=int(p.parent.name[1:]),
                                  report_file=str(Path('data/runs') / p.relative_to(RUNS)),
                                  characters=len(p.read_text())) for p in reports]), 'survey/codex_reports.csv')
    prepare_ratings()


def prepare_ratings():
    ratings = pd.read_csv(INPUTS / 'survey/finding_ratings.csv')
    items = pd.read_csv(INPUTS / 'survey/findings.csv')
    pairs = pd.read_csv(INPUTS / 'survey/comparisons.csv')
    pair_ratings = pd.read_csv(INPUTS / 'survey/pair_ratings.csv')
    dimensions = ('confidence', 'novelty', 'reasoning_support', 'priority')
    ratings['composite_score'] = ratings[[name + '_score' for name in dimensions[1:]]].mean(axis=1)
    summary = []
    for finding, group in ratings.groupby('finding_id', sort=False):
        row = {'finding_id': finding, 'n_reviewers': group.reviewer_id.nunique()}
        for dimension in (*dimensions, 'composite'):
            score = group[dimension + '_score']
            row.update({f'n_{dimension}': score.count(), f'mean_{dimension}': score.mean(), f'sd_{dimension}': score.std()})
        summary.append(row)
    findings = items.merge(pd.DataFrame(summary), on='finding_id', validate='one_to_one')
    if len(findings) != 60 or len(ratings) != 180 or ratings.duplicated(['reviewer_id', 'finding_id']).any():
        raise ValueError('Expected 180 unique ratings for 60 survey findings')
    buckets = []
    for bucket, group in ratings.groupby('bucket', sort=True):
        row = dict(bucket=bucket, bucket_description=group.bucket_description.iloc[0],
                   source=group.source.iloc[0], n_findings=group.finding_id.nunique(), n_evaluations=len(group))
        item_means = findings[findings.bucket.eq(bucket)]
        row.update({f'mean_{d}': item_means['mean_' + d].mean() for d in (*dimensions, 'composite')})
        buckets.append(row)
    score = pair_ratings.raw_display_preference_score
    pair_ratings['distributed_agents_preference_score'] = score.where(pair_ratings.display_B_source.eq('Distributed Agents'), 6 - score)
    summary = []
    for comparison, group in pair_ratings.groupby('comparison_id', sort=False):
        score = group.distributed_agents_preference_score
        summary.append(dict(comparison_id=comparison, n_responses=len(group), n_scored=score.count(),
                            mean_distributed_agents_preference=score.mean(), sd_distributed_agents_preference=score.std(),
                            n_prefer_distributed_agents=score.gt(3).sum(), n_tie=score.eq(3).sum(),
                            n_prefer_codex=score.lt(3).sum(), n_cannot_assess=score.isna().sum(),
                            n_distributed_agents_shown_first=group.display_A_source.eq('Distributed Agents').sum(),
                            n_codex_shown_first=group.display_A_source.eq('Codex').sum()))
    pairs = pairs.merge(pd.DataFrame(summary), on='comparison_id', validate='one_to_one')
    if len(pairs) != 20 or len(pair_ratings) != 60:
        raise ValueError('Expected 60 paired evaluations of 20 comparisons')
    for name, frame in [('finding_summary', findings), ('finding_ratings', ratings),
                        ('bucket_summary', pd.DataFrame(buckets)), ('pair_summary', pairs), ('pair_ratings', pair_ratings)]:
        write_table(frame, f'survey/{name}.csv')
