function A = check_genre_predictions(data, genre, fraction_to_train, num_trials)

failed_fractions = [];

for j = 1:num_trials
    [num_movies, num_features] = size([data]); 

    rand_order = randperm(num_movies); % random ordering

    train_to = floor(fraction_to_train*num_movies); 

    train_data = data(rand_order(1:train_to),:);
    test_data = data(rand_order(train_to+1:end),:);
    train_labels =  genre(rand_order(1:train_to));
    test_labels = genre(rand_order(train_to+1:end));

    tree = fitctree(train_data, train_labels); % train on the first 80% of movies

    prediction = predict(tree,test_data);
    failed_fraction = sum(abs(test_labels-prediction))/(num_movies-train_to);
    failed_fractions(j) = failed_fraction;
    
end
% view(tree)

A = sum(failed_fractions)/length(failed_fractions);