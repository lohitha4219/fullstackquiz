from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from quiz.models import Result


@login_required
def leaderboard(request, domain=None):

    # ✅ Filter by domain if selected
    if domain:
        results = Result.objects.filter(domain=domain)
    else:
        results = Result.objects.all()

    # 🥇 highest score per user
    top_scores = (
        results
        .values("user__username", "user")
        .annotate(max_score=Max("score"))
        .order_by("-max_score")[:100]
    )

    leaderboard_data = []
    user_rank = None
    rank = 1

    for entry in top_scores:
        data = {
            "rank": rank,
            "username": entry["user__username"],
            "score": entry["max_score"],
            "is_me": entry["user"] == request.user.id
        }

        if data["is_me"]:
            user_rank = rank

        leaderboard_data.append(data)
        rank += 1

    return render(request, "leaderboard.html", {
        "leaderboard": leaderboard_data,
        "domain": domain,
        "user_rank": user_rank
    })