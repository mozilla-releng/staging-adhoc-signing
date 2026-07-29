# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from taskgraph.target_tasks import register_target_task


@register_target_task("h1_benign_probe")
def target_tasks_h1_benign_probe(full_task_graph, parameters, graph_config):
    """Select only the restoring hardlink healthcheck probe."""
    return [
        label
        for label in (
            "fetch-h1-tar-hardlink-healthcheck-probe",
            "dep-signing-h1-tar-hardlink-healthcheck-probe",
        )
        if label in full_task_graph.tasks
    ]


@register_target_task("promote_adhoc")
def target_tasks_promote(full_task_graph, parameters, graph_config):
    """Select the set of tasks required for promoting adhoc signing."""

    def filter(task, parameters):
        if task.attributes.get('shipping-phase') not in ('build', 'promote'):
            return False
        manifest_name = task.attributes.get('manifest', {}).get('manifest_name')
        if manifest_name and manifest_name == parameters["adhoc_name"]:
            return True

    return [l for l, t in full_task_graph.tasks.items() if filter(t, parameters)]
