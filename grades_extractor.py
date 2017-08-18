#!/usr/bin/env python3
import helper

def main():
    args = get_args()
    with_notenspiegel = not args.without_notenspiegel
    grades = helper.get_grades(with_notenspiegel, force_new = args.force_new)

    for grade_data in grades:
        grade = grade_data['grade']
        title = grade_data['title']
        if grade == 5.0:
            continue
        print("{}\t{}".format(grade, title.encode('utf-8')))
    
    if with_notenspiegel:
        diffs = []
        diffs_without_failed = []
        for grade in grades:
            grade = grade_data['grade']
            avg = helper.get_avg_from_notenspiegel(grade_data['notenspiegel'])
            if avg < 1:
                continue
            avg_without_failed = helper.get_avg_from_notenspiegel_without_failed(grade_data['notenspiegel'])
            diff = avg - grade
            diff_without_failed = avg_without_failed - grade
            diffs.append(diff)
            diffs_without_failed.append(diff_without_failed)

        def get_diff_avg_for_notenspiegel(diffs):
            return sum(diffs) / len(diffs)
        avg_of_diff_to_avgs = get_diff_avg_for_notenspiegel(diffs)
        avg_of_diff_to_avgs_without_failed = get_diff_avg_for_notenspiegel(diffs_without_failed)
        print('avg diff: {}'.format(round(avg_of_diff_to_avgs, 2)))
        print('avg diff without failed: {}'.format(round(avg_of_diff_to_avgs_without_failed, 2)))

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Extract grades from tucan', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--without-notenspiegel', action='store_true', help='Whether the notenspiegel is NOT extracted. Saves some crawling time.')
    parser.add_argument('--force-new', action='store_true', help='Whether to download the grades again.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()