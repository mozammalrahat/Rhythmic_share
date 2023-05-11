import graphene
from .models import Track, Like, Comment, MusicReview
from graphene_django import DjangoObjectType
from users.schema import UserType
from django.db.models import Q


class TrackType(DjangoObjectType):

    class Meta:
        model = Track


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class MusicReviewType(DjangoObjectType):
    class Meta:
        model = MusicReview


class Query(graphene.ObjectType):

    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)
    Comments = graphene.List(CommentType)
    MusicReviews = graphene.List(MusicReviewType)

    def resolve_tracks(self, info, search=None):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(url__icontains=search) |
                Q(posted_by__username__icontains=search)

            )
            return Track.objects.filter(filter)
        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()

    def resolve_comments(self, info):
        return Comment.objects.all()

    def resolve_music_reviews(self, info):
        return MusicReview.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Log in to add Track")
        track = Track(title=title, description=description, url=url,
                      posted_by=user)
        track.save()

        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, description, url):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception("Not permitted to update this track")

        track.title = title
        track.description = description
        track.url = url

        track.save()

        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if track.posted_by != user:
            raise Exception("Not Permitted to Delete this Track.")
        track.delete()

        return DeleteTrack(track_id=track_id)


class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Login to like tracks.")

        track = Track.objects.get(id=track_id)

        if not track:
            raise Exception("Cannot find track with given track id")
        Like.objects.create(
            user=user,
            track=track
        )

        return CreateLike(user=user, track=track)


class createComment(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)
    body = graphene.String()

    class Arguments:
        track_id = graphene.Int(required=True)
        body = graphene.String(required=True)

    def mutate(self, info, track_id, body):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if user.is_anonymous:
            raise Exception("Login to comment on tracks.")
        Comment.objects.create(
            user=user,
            track=track,
            body=body
        )
        return createComment(user=user, track=track, body=body)


class updateComment(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)
    body = graphene.String()

    class Arguments:
        track_id = graphene.Int(required=True)
        body = graphene.String(required=True)

    def mutate(self, info, track_id, body):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if user.is_anonymous:
            raise Exception("Login to comment on tracks.")
        Comment.objects.update(
            user=user,
            track=track,
            body=body
        )
        return updateComment(user=user, track=track, body=body)


class deleteComment(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)
    body = graphene.String()

    class Arguments:
        track_id = graphene.Int(required=True)
        body = graphene.String(required=True)

    def mutate(self, info, track_id, body):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if user.is_anonymous:
            raise Exception("Login to comment on tracks.")
        Comment.objects.delete(
            user=user,
            track=track,
            body=body
        )
        return deleteComment(user=user, track=track, body=body)


class CreateMusicReview(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)
    body = graphene.String()

    class Arguments:
        track_id = graphene.Int(required=True)
        body = graphene.String(required=True)

    def mutate(self, info, track_id, body):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if user.is_anonymous:
            raise Exception("Login to comment on tracks.")
        MusicReview.objects.create(
            user=user,
            track=track,
            body=body
        )
        return CreateMusicReview(user=user, track=track, body=body)


class updateMusicReview(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)
    body = graphene.String()

    class Arguments:
        track_id = graphene.Int(required=True)
        body = graphene.String(required=True)

    def mutate(self, info, track_id, body):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if user.is_anonymous:
            raise Exception("Login to comment on tracks.")
        MusicReview.objects.update(
            user=user,
            track=track,
            body=body
        )
        return updateMusicReview(user=user, track=track, body=body)


class deleteMusicReview(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)
    body = graphene.String()

    class Arguments:
        track_id = graphene.Int(required=True)
        body = graphene.String(required=True)

    def mutate(self, info, track_id, body):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if user.is_anonymous:
            raise Exception("Login to comment on tracks.")
        MusicReview.objects.delete(
            user=user,
            track=track,
            body=body
        )
        return deleteMusicReview(user=user, track=track, body=body)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
    create_comment = createComment.Field()
    update_comment = updateComment.Field()
    delete_comment = deleteComment.Field()
    create_music_review = CreateMusicReview.Field()
    update_music_review = updateMusicReview.Field()
    delete_music_review = deleteMusicReview.Field()
