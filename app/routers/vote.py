from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
        current_user: int = Depends(oauth2.get_current_user)):

    #query if post exist
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {vote.post_id} not exist')

    # query db to see if there is already an exist vote
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                    models.Vote.user_id == current_user.id)


    found_vote = vote_query.first()

    # vote.dir == 1 to add vote
    if (vote.dir == 1):

        # if this vote already exist raise 409
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        
        # if this vote does not exist then add to db

        # create new_vote entry
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        
        # add to db
        db.add(new_vote)
        db.commit()
        return {"message", "successgully added vote"}
    
    # vote.dir = 0 to remove vote
    else:
        # if the vote does not exist then raise 404 sincce cant remove vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="Vote does not exist")

        # if vote does exist then delete from db
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message", "successfully deleted vote"}

